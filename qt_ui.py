import sys
import typing

from PyQt6.QtCore import (
    QObject,
    QSize,
    Qt,
    QTimer,
    QThread,
    pyqtSignal,
    QAbstractTableModel,
    QModelIndex,
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QMessageBox,
    QTableView,
    QTextEdit,
    QLineEdit,
    QCheckBox,
    QSlider,
)
from PyQt6.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from page import ScorePages
import sys


class SeparatorUI(QMainWindow):

    def __init__(self, pages:ScorePages, width=1200, height=800):
        super().__init__()
        self.score_pager = pages
        self.setWindowTitle("Separator")
        
        self.overall_height = height
        self.setGeometry(100, 100, width, self.overall_height)
        self._draw_layout()
        # self._load_image_to_prev("sample.png")
        # self._load_image("sample.png")

        # structure for annotation
        self.anno_coords = []
        self.last_anno_coords = []
        self.pixel_map_histories = []

        # setup on the first page
        self.current_file = pages.score_image_files[self.score_pager.current_index]
        self._load_image(self.current_file)

    # layout construction
    def _draw_layout(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.internal_height = self.overall_height
        # The very variable for indicating the relevant position of the segment lines
        self.prev_pixel_label = QLabel()
        self.annotate_bar = QSlider(Qt.Orientation.Vertical)
        self.annotate_bar.setRange(0, self.internal_height)
        self.annotate_bar.setSingleStep(2)
        # display should also follow the internal height

        self.current_pixel_label = QLabel()
        self.main_layout.addWidget(self.prev_pixel_label)
        self.main_layout.addWidget(self.annotate_bar)
        self.main_layout.addWidget(self.current_pixel_label)
        self.op_btns_layout = QVBoxLayout()
        # top alignment
        self.op_btns_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.addLayout(self.op_btns_layout)
        self.annotate_bar.valueChanged.connect(self._draw_following_line)
        # self.annotate_bar.sliderMoved.connect(self._draw_following_line_preview)

        self.next_page_btn = QPushButton("Next Page")
        
        self.undo_btn = QPushButton("Undo")
        self.discard_page_btn = QPushButton("Discard Page")
        self.discard_annotation_btn = QPushButton("Discard Annotation")
        self.export_btn = QPushButton("Export")
        # add them
        self.op_btns_layout.addWidget(self.next_page_btn)
        self.op_btns_layout.addWidget(self.undo_btn)
        self.op_btns_layout.addWidget(self.discard_page_btn)
        self.op_btns_layout.addWidget(self.discard_annotation_btn)
        self.op_btns_layout.addWidget(self.export_btn)

        # connect
        self.next_page_btn.clicked.connect(self._next_page)
        self.undo_btn.clicked.connect(self._undo_last_line)
        self.discard_annotation_btn.clicked.connect(self._discard_annotation)
        self.discard_page_btn.clicked.connect(self._discard_page)
        self.export_btn.clicked.connect(self._export)

        self.info_label = QLabel()
        self.op_btns_layout.addWidget(self.info_label)

    def _clearance_marks(self):
        self.annotate_bar.setValue(0)
        self.anno_coords.clear()
        self.pixel_map_histories.clear()

    def _discard_annotation(self):
        self._clearance_marks()
        self._load_image(self.current_file, keep_annotation=False)

    # def _load_image_to_prev(self, image_path):
    #     pixmap = QPixmap(image_path)
    #     # scale pixmap
    #     pixmap = pixmap.scaledToHeight(self.internal_height)
    #     self.prev_pixel_label.setPixmap(pixmap)

    def _load_image(self, image_path, keep_annotation=True):
        pixmap = QPixmap(image_path)
        # scale pixmap
        pixmap = pixmap.scaledToHeight(self.internal_height)
        self.current_pixel_label.setPixmap(pixmap)
        self.info_label.setText(f"Current working on: {image_path}")
        if keep_annotation:
            self._apply_last_coords()

    def _export(self):
        self.score_pager.export()
        QMessageBox.information(self, "Info", "Export complete")

    def _check_annotation_complete(self):
        if len(self.anno_coords) != len(self.score_pager.instrument_config["instruments"]):
            QMessageBox.information(self, "Info", f"Annotation incomplete or too much, need {len(self.score_pager.instrument_config['instruments'])} but found {len(self.anno_coords)}")
            return False
        self.score_pager.slice_current_page(list(map(lambda x: x/self.internal_height,self.anno_coords))+[1])
        QMessageBox.information(self, "Info", "Annotation complete and recorded")
        self.last_anno_coords = self.anno_coords.copy()
        self._clearance_marks()
        return True
    
    def _apply_last_coords(self):
        for p in self.last_anno_coords:
            self._draw_following_line(self.internal_height - p)

    def _next_page(self):
        if self._check_annotation_complete():
            if self.score_pager.current_index < len(self.score_pager.score_image_files) - 1:
                # current page to the left as a reference
                self.prev_pixel_label.setPixmap(self.current_pixel_label.pixmap())
                self.score_pager.current_index += 1
                self.current_file = self.score_pager.score_image_files[self.score_pager.current_index]
                self._load_image(self.current_file)
            else:
                QMessageBox.information(self, "Info", "This is already the last page")

    def _draw_following_line(self, pixel):
        # draw a line on the current pixel label
        if pixel == 0:
            return
        pixel = self.internal_height - pixel
        pixel_map = self.current_pixel_label.pixmap()
        last_pixel_map = pixel_map.copy()
        painter = QPainter(pixel_map)
        pen = QPen(QColor(255, 0, 0), 1)
        painter.setPen(pen)
        painter.drawLine(
            0, pixel, 600, pixel
        )  # Example drawing
        painter.end()
        self.current_pixel_label.setPixmap(pixel_map)

        # save the history
        self.pixel_map_histories.append(last_pixel_map)
        self.anno_coords.append(pixel)

    def _draw_following_line_preview(self, pixel):
        # FIXME: Deprecated
        # draw a line on the current pixel label
        # FIXME: Not very simple to implement
        if len(self.pixel_map_histories) > 0:
            self.current_pixel_label.setPixmap(self.pixel_map_histories[-1])
        pixel = self.internal_height - pixel
        pixel_map = self.current_pixel_label.pixmap()
        last_pixel_map = pixel_map.copy()
        painter = QPainter(pixel_map)
        pen = QPen(QColor(255, 0, 0), 1)
        painter.setPen(pen)
        painter.drawLine(
            0, pixel, 600, pixel
        )  # Example drawing
        painter.end()
        self.current_pixel_label.setPixmap(pixel_map)

        # save the history
        self.pixel_map_histories.append(last_pixel_map)
        # self.anno_coords.append(pixel)

    def _undo_last_line(self):
        if len(self.pixel_map_histories) > 0:
            last_pixel_map = self.pixel_map_histories.pop()
            self.current_pixel_label.setPixmap(last_pixel_map)
            self.anno_coords.pop()

    def _discard_page(self):
        # Answerbox first to confirm discarding the page
        reply = QMessageBox.question(
            self,
            "Warning",
            "Are you sure to discard the current page?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._clearance_marks()
            self.score_pager.score_image_files.pop(self.score_pager.current_index)
            if self.score_pager.current_index == len(self.score_pager.score_image_files):
                self.score_pager.current_index -= 1 # tail corner
            self.current_file = self.score_pager.score_image_files[self.score_pager.current_index]
            self._load_image(self.current_file)
            