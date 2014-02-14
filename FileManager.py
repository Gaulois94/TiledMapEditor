from gi.repository import Gtk
from os import path
import xml.etree.ElementTree as ET
import globalVar

class FileManager():
    def __init__(self, parent):
        self.parent = parent
        self.xmlFile = str()

    def _getFileName(self, dialog, filt):
        self.setFilter(dialog, filt)
        response = dialog.run()

        filename = None
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        dialog.destroy()
        return filename

    def _openFile(self, mime):
        dialog = Gtk.FileChooserDialog("Choose a file", self.parent,\
                Gtk.FileChooserAction.OPEN, (Gtk.STOCK_OPEN, Gtk.ResponseType.OK,\
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        return self._getFileName(dialog, mime)

    def openFileXML(self, tileBox, traceManager):
        fileName = self._openFile("xml")
        xmlTree = ET.parse(fileName)
        xmlRoot = xmlTree.getroot()
        tileBox.decodeXML(xmlRoot.find('Files'), path.dirname(fileName))
        #globalVar.tileWindow.decodeXML(xmlRoot.find('Window'))

    def openFileImage(self):
        return self._openFile('image')

    def saveAsFile(self, tileBox, traceManager):
        dialog = Gtk.FileChooserDialog("Where to save the map ?", self.parent, \
                Gtk.FileChooserAction.SAVE, (Gtk.STOCK_SAVE, Gtk.ResponseType.OK, \
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
        self.xmlFile = self._getFileName(dialog, filt="xml")
        self.saveFile(tileBox, traceManager)

    def saveFile(self, tileBox, traceManager):
        xmlRoot = ET.fromstring('<map></map>')
        xmlRoot.append(globalVar.tileWindow.getSaveFileElem())
        xmlRoot.append(tileBox.getSaveFileElem())
        xmlRoot.append(traceManager.getSaveFileElem(tileBox))

        with open(self.fileName, 'w') as xmlFile:
            xmlFile.write(str(ET.tostring(xmlRoot).decode()))

    def setFilter(self, dialog, filt):
        if filt=="xml":
            filterXML = Gtk.FileFilter()
            filterXML.set_name("XML File")
            filterXML.add_mime_type("application/xml")
            dialog.add_filter(filterXML)
        elif filt=="image":
            filterImage = Gtk.FileFilter()
            filterImage.set_name("Image File")
            filterImage.add_mime_type("image/png")
            filterImage.add_mime_type("image/jpeg")
            filterImage.add_mime_type("image/bmp")
            dialog.add_filter(filterImage)
