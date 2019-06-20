from PyQt5.QtCore import QRectF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap, QPen
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem

 
class GraphicsView(QGraphicsView):
    save_signal = pyqtSignal(bool)
 
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)
 
    def setItem(self,imageItem):
        self.image_item = GraphicsPixmapItem(imageItem)
        self.image_item.setFlag(QGraphicsItem.ItemIsMovable)

    def Scene(self):
        self.scene = QGraphicsScene()
        self.scene.addItem(self.image_item)
        self.setScene(self.scene)

    def mouseReleaseEvent(self, event):
        if self.image_item.is_finish_cut:
            self.save_signal.emit(True)
        else:
            self.save_signal.emit(False)
 
 
class GraphicsPixmapItem(QGraphicsPixmapItem):
    save_signal = pyqtSignal(bool)
    def __init__(self, picture, parent=None):
        super(GraphicsPixmapItem, self).__init__(parent)
        self.setPixmap(picture)
        self.isStart = False
        self.current_point = None
        self.is_finish_cut = False

    def setStart(self,flag):
        self.isStart = flag
        self.update()

    def mouseMoveEvent(self, event):
        self.current_point = event.pos()
        self.is_finish_cut = False
        self.update()
 
    def mousePressEvent(self, event):
        super(GraphicsPixmapItem, self).mousePressEvent(event)
        self.start_point = event.pos()
        self.current_point = None
        self.is_finish_cut = False
        self.update()
        
    def paint(self, painter, QStyleOptionGraphicsItem, QWidget):
        super(GraphicsPixmapItem, self).paint(painter, QStyleOptionGraphicsItem, QWidget)
        if self.isStart == True:
            pen = QPen()
            pen.setColor(QColor(255, 0, 0))
            pen.setWidth(3)
            painter.setPen(pen)
            if not self.current_point:
                return
            painter.drawRect(QRectF(self.start_point, self.current_point))
            self.end_point = self.current_point
            self.is_finish_cut = True
            self.update()