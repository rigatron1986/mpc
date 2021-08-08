import sys

from PySide2 import QtWidgets, QtCore


class TurnTableUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(TurnTableUI, self).__init__(parent)
        self.resize(430, 170)
        self.setMinimumSize(430, 170)
        self.setMaximumSize(430, 170)
        self.main_grid = QtWidgets.QGridLayout(self)
        self.vertical_layout_01 = QtWidgets.QVBoxLayout(self)

        self.camera_buttons_h_layout = QtWidgets.QHBoxLayout()
        self.create_camera = QtWidgets.QPushButton(self)
        self.create_camera.setText("create_camera")
        self.camera_buttons_h_layout.addWidget(self.create_camera)
        self.delete_camera = QtWidgets.QPushButton(self)
        self.delete_camera.setText("delete_camera")
        self.camera_buttons_h_layout.addWidget(self.delete_camera)
        self.vertical_layout_01.addLayout(self.camera_buttons_h_layout)

        """
        distance slider_group
        """
        self.distance_h_layout_01 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Distance")
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.distance_h_layout_01.addWidget(self.label)
        self.distance_le = QtWidgets.QLineEdit(self)
        self.distance_le.setEnabled(False)
        self.distance_le.setMaximumSize(QtCore.QSize(60, 500))
        self.distance_h_layout_01.addWidget(self.distance_le)
        self.distance_slider = QtWidgets.QSlider(self)
        self.distance_slider.setMinimum(-100)
        self.distance_slider.setMaximum(100)
        self.distance_slider.setOrientation(QtCore.Qt.Horizontal)
        self.distance_h_layout_01.addWidget(self.distance_slider)
        self.vertical_layout_01.addLayout(self.distance_h_layout_01)

        """
        height slider group
        """
        self.height_h_layout_01 = QtWidgets.QHBoxLayout()
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setText('Height')
        self.label_2.setMinimumSize(QtCore.QSize(60, 0))
        self.height_h_layout_01.addWidget(self.label_2)
        self.height_le = QtWidgets.QLineEdit(self)
        self.height_le.setEnabled(False)
        self.height_le.setMaximumSize(QtCore.QSize(60, 500))
        self.height_h_layout_01.addWidget(self.height_le)
        self.height_slider = QtWidgets.QSlider(self)
        self.height_slider.setMinimum(-100)
        self.height_slider.setMaximum(100)
        self.height_slider.setOrientation(QtCore.Qt.Horizontal)
        self.height_h_layout_01.addWidget(self.height_slider)
        self.vertical_layout_01.addLayout(self.height_h_layout_01)

        """
        turn angle slider group
        """
        self.turn_h_layout_01 = QtWidgets.QHBoxLayout()
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setText('Turn Angle')
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.turn_h_layout_01.addWidget(self.label_3)
        self.turn_angel_le = QtWidgets.QLineEdit(self)
        self.turn_angel_le.setEnabled(False)
        self.turn_angel_le.setMaximumSize(QtCore.QSize(60, 500))
        self.turn_h_layout_01.addWidget(self.turn_angel_le)
        self.turn_angel_slider = QtWidgets.QSlider(self)
        self.turn_angel_slider.setMinimum(1)
        self.turn_angel_slider.setMaximum(360)
        self.turn_angel_slider.setOrientation(QtCore.Qt.Horizontal)
        self.turn_h_layout_01.addWidget(self.turn_angel_slider)
        self.vertical_layout_01.addLayout(self.turn_h_layout_01)

        """
        play_blast button
        """
        self.play_blast_btn = QtWidgets.QPushButton(self)
        self.play_blast_btn.setText('Create Playblast')

        self.vertical_layout_01.addWidget(self.play_blast_btn)
        self.main_grid.addLayout(self.vertical_layout_01, 0, 0, 1, 1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TurnTableUI()
    ui.show()
    sys.exit(app.exec_())
