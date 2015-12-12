import os
from PySide import QtGui, QtCore
import managers
import sys
import ecowrap
import re
import qdarkstyle


class Launcher(QtGui.QMainWindow):
    '''Main window
    '''

    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent=parent)
        # Setup the UI
        self.setupUi()
        self.projects = {}

        # Create the application and project managers
        self.app_manager = managers.ApplicationManager()
        self.prj_manager = managers.ProjectManager()

        # Fill the applications and the projects with them
        for key, val in self.app_manager.applications.items():
            self.add_app(
                name=val.get('label'),
                icon=val.get('icon'),
                data=val
            )

        for key, val in self.prj_manager.projects.items():
            self.add_project(
                name=val.get('name'),
                label=val.get('label'),
                tools=val.get('tools')
            )

    def setupUi(self):
        '''Sets up the launcher UI.'''

        self.setWindowTitle('Application Launcher')
        rocket_path = os.path.join(
            os.path.dirname(__file__),
            'resources',
            'rocket.png'
        )
        pixmap = QtGui.QPixmap(rocket_path)
        self.setWindowIcon(QtGui.QIcon(pixmap))

        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.resize(600, 400)

        self.central_widget = QtGui.QWidget(self)
        self.central_layout = QtGui.QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        self.project_layout = QtGui.QHBoxLayout()
        spacerItem = QtGui.QSpacerItem(
            40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.project_label = QtGui.QLabel('Project:')
        self.project_combo = QtGui.QComboBox(self.central_widget)
        self.project_layout.addItem(spacerItem)
        self.project_layout.addWidget(self.project_label)
        self.project_layout.addWidget(self.project_combo)

        self.app_container = QtGui.QFrame(self.central_widget)
        self.app_layout = FlowLayout()
        self.app_container.setLayout(self.app_layout)

        self.log = QtGui.QTextEdit(self.central_widget)
        self.log.setReadOnly(True)
        self.log.hide()

        self.central_layout.addLayout(self.project_layout)
        self.central_layout.addWidget(self.app_container)
        self.central_layout.addWidget(self.log)

    def add_app(self, name, icon, data):
        '''Creates a new instance of an ApplicationButton with the data
        in the arguments and adds it to the application's FlowLayout

        :param name: Name of the application
        :param icon: Icon of the application
        :param data: Raw data from the ApplicationManager
        :type name: str
        :type icon: str
        :type data: dict
        '''
        btn = ApplicationButton(
            name=name,
            icon=icon,
            data=data,
            parent=self.app_container,
        )
        btn.clicked.connect(self.on_button_clicked)
        self.app_layout.addWidget(btn)

    def add_project(self, name, label, tools):
        '''Creates a new entry to the project's ComboBox. It also stores
        the required tools in self.projects to fetch it later.

        :param name: Name of the project
        :param label: Label of the project
        :param tools: Tools used for the project
        :type name: str
        :type label: str
        :type tools: dict
        '''
        self.projects[label] = tools
        self.project_combo.addItem(
            label,
            None,
        )

    def on_button_clicked(self):
        '''Executes the application and the project specified.
        '''
        # Get the button who called the action
        btn = self.sender()

        # Extract the info from que button
        app_tool = btn.data.get('tool')
        app_id = btn.data.get('id')
        app_exec = btn.data.get('executable')

        # Get the current project
        project = self.project_combo.currentText()

        # Match the project tools with the App ID and add them.
        tools = [app_tool]
        for key, val in self.projects[project].items():
            if re.compile(key).match(app_id):
                tools += val

        # Launch the command and if it fails, report it.
        try:
            self.launch_eco(tools=tools, executable=app_exec)
        except Exception:
            import traceback
            self.log.setHidden(False)
            self.log.append(traceback.format_exc())

    def launch_eco(self, tools, executable):
        ecowrap.run(tools=tools, executable=executable)


class ApplicationButton(QtGui.QToolButton):

    def __init__(self, name, icon=None, data=None, parent=None):
        super(ApplicationButton, self).__init__(parent=parent)
        self.data = data

        self.setMinimumSize(QtCore.QSize(100, 100))
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setText(name)

        # For relative paths, we look in the 'resources' folder
        if not os.path.isfile(icon):
            icon = os.path.join(
                os.path.dirname(__file__), 'resources', icon)

        self.setIcon(
            QtGui.QIcon(
                QtGui.QPixmap(icon)
            )
        )
        self.setIconSize(QtCore.QSize(50, 50))


class FlowLayout(QtGui.QLayout):

    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setMargin(margin)

        self.setSpacing(spacing)

        self.itemList = []

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        size += QtCore.QSize(2 * self.contentsMargins().top(),
                             2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            spaceX = self.spacing() + wid.style().layoutSpacing(
                QtGui.QSizePolicy.PushButton,
                QtGui.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            spaceY = self.spacing() + wid.style().layoutSpacing(
                QtGui.QSizePolicy.PushButton,
                QtGui.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y()


def main():
    app = QtGui.QApplication('pipelauncher')
    launcher = Launcher()

    launcher.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
