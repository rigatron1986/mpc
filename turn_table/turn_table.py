# -*- coding: utf-8 -*-
import sys
from collections import OrderedDict
from PySide2 import QtWidgets

from turn_table_UI import TurnTableUI
import core

maya_ui = core.get_maya_window()
turn_table_creator = core.TurnTableCreator()

"""
import mpc.turn_table.turn_table as turn_table_ui
reload(turn_table_ui)
turn_table_ui.import_ui()
"""


class TurnTable(TurnTableUI):
    def __init__(self, parent=maya_ui):
        super(TurnTable, self).__init__(parent)
        self.setWindowTitle("Turntable creator")
        self.set_defaults()
        self.init_connections()

    def set_defaults(self):
        """
        Sets all the attributes to default values
        :return: None
        """
        self.distance_le.setEnabled(True)
        self.distance_le.setText(str(0))
        self.distance_le.setEnabled(False)
        self.distance_slider.setValue(0)

        self.height_le.setEnabled(True)
        self.height_le.setText(str(0))
        self.height_le.setEnabled(False)
        self.height_slider.setValue(0)

        self.turn_angel_le.setEnabled(True)
        self.turn_angel_le.setText(str(1))
        self.turn_angel_le.setEnabled(False)
        self.turn_angel_slider.setValue(1)

    def init_connections(self):
        """
        Creates all the connections
        :return:None
        """
        self.create_camera.clicked.connect(lambda: self.create_camera_group())
        self.delete_camera.clicked.connect(lambda: self.delete_camera_group())
        self.play_blast_btn.clicked.connect(lambda: self.create_play_blast())
        self.distance_slider.valueChanged.connect(self.distance_slider_setter)
        self.height_slider.valueChanged.connect(self.height_slider_setter)
        self.turn_angel_slider.valueChanged.connect(self.turn_angle_slider_setter)

    def distance_slider_setter(self, value):
        self.distance_le.setEnabled(True)
        self.distance_le.setText(str(value))
        self.distance_le.setEnabled(False)
        turn_table_creator.set_camera_position('distance', value)

    def height_slider_setter(self, value):
        self.height_le.setEnabled(True)
        self.height_le.setText(str(value))
        self.height_le.setEnabled(False)
        turn_table_creator.set_camera_position('height', value)

    def turn_angle_slider_setter(self, value):
        self.turn_angel_le.setEnabled(True)
        self.turn_angel_le.setText(str(value))
        self.turn_angel_le.setEnabled(False)

    def create_camera_group(self):
        print('check if camera group is present, if not create camera group')
        result = turn_table_creator.create_camera()
        if not result:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("turn_table_grp present.\nDelete and try again.")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        print(result)
        self.set_defaults()

    @staticmethod
    def delete_camera_group():
        print('check if camera group is present, if present delete it')
        result = turn_table_creator.delete_turn_table_group()
        print(result)

    @staticmethod
    def get_key_frames(turn_angle):
        to_key = OrderedDict()
        val = 360 / turn_angle

        for x in range(val + 1):
            to_key[x + 1] = x * turn_angle

        last_key = to_key.keys()[-1]
        last_value = to_key[to_key.keys()[-1]]
        if last_value < 360:
            to_key[last_key + 1] = 360
        else:
            to_key[last_key] = 360
        return to_key

    def create_play_blast(self):
        print('creating play blast')
        turn_angle = self.turn_angel_slider.value()
        key_frames = self.get_key_frames(turn_angle)
        play_blast_path = turn_table_creator.create_playblast(key_frames)
        print(play_blast_path)
        if play_blast_path:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Play blast exported to \n{play_blast_path}".format(play_blast_path=play_blast_path))
            msg.setWindowTitle("Success")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()


def import_ui():
    global WIN
    try:
        WIN.close()
        WIN.deleteLater()
    except Exception as e:
        print(e)
        pass
    WIN = TurnTable()
    WIN.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TurnTable()
    ui.show()
    sys.exit(app.exec_())
