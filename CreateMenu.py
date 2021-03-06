from gi.repository import Gtk, Gdk, GdkPixbuf
import globalVar
import sfml as sf
import functions

class CreateMenu:
    def __init__(self, parent):
        self.parent = parent

    def newFile(self, fileManager):
        window = Gtk.Window(title="New File")
        window.set_property("modal",True)
        accelGroup = Gtk.AccelGroup()
        window.add_accel_group(accelGroup)

        vgrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        grid = Gtk.Grid()
        nameLabel = Gtk.Label("Name")
        formatLabel = Gtk.Label("Tile Format")
        numberCases = Gtk.Label("Number Cases")

        grid.attach(nameLabel, 0, 0, 1, 1)
        grid.attach_next_to(formatLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(numberCases, formatLabel, Gtk.PositionType.BOTTOM, 1, 1)

        nameEntered = Gtk.Entry()
        nameEntered.set_text("Tile")

        #Tile Format widgets
        xLabel = Gtk.Label("x")
        spinTileLeft = Gtk.SpinButton()
        adjustment1 = Gtk.Adjustment(32, 1, 1000, 1, 10, 0)
        spinTileLeft.set_adjustment(adjustment1)
        adjustment2 = Gtk.Adjustment(32, 1, 1000, 1, 10, 0)
        spinTileRight = Gtk.SpinButton()
        spinTileRight.set_adjustment(adjustment2)

        #Number cases widgets
        xBisLabel = Gtk.Label("x")
        spinCasesLeft = Gtk.SpinButton()
        adjustment3 = Gtk.Adjustment(32, 1, 100000, 1, 10, 0)
        spinCasesLeft.set_adjustment(adjustment3)
        adjustment4 = Gtk.Adjustment(32, 1, 100000, 1, 10, 0)
        spinCasesRight = Gtk.SpinButton()
        spinCasesRight.set_adjustment(adjustment4)

        grid.attach_next_to(nameEntered, nameLabel, Gtk.PositionType.RIGHT, 3, 1)

        grid.attach_next_to(spinTileLeft, formatLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(xLabel, spinTileLeft, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(spinTileRight, xLabel, Gtk.PositionType.RIGHT, 1, 1)

        grid.attach_next_to(spinCasesLeft, numberCases, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(xBisLabel, spinCasesLeft, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(spinCasesRight, xBisLabel, Gtk.PositionType.RIGHT, 1, 1)

        vgrid.add(grid)
        hbox = Gtk.Box()

        okButton = Gtk.Button(label="OK")
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_Return, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_KP_Enter, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.connect("clicked", self.initNewFile, \
                {'hTileSize':spinTileLeft, 'vTileSize':spinTileRight, \
                'hNumberCases':spinCasesLeft, 'vNumberCases':spinCasesRight, \
                'nameEntered':nameEntered, 'window':window})

        cancelButton = Gtk.Button(label="Cancel")
        cancelButton.add_accelerator("activate", accelGroup, Gdk.KEY_Escape, 0, \
                Gtk.AccelFlags.MASK)
        cancelButton.connect("clicked", self.quitWindow, window)

        hbox.pack_start(cancelButton, False, False, 0)
        hbox.pack_start(okButton, False, False, 0)
        vgrid.add(hbox)
        hbox.set_halign(Gtk.Align.END)
        hbox.set_valign(Gtk.Align.END)

        window.connect("destroy", self.quitWindow, window, "cancel")
        window.add(vgrid)
        window.show_all()

    def createNewImage(self, fileManager, tileBox):
        if globalVar.sfmlArea:
            window = Gtk.Window(title="New image")
            window.set_property("modal",True)

            notebook = Gtk.Notebook()
            notebook.append_page(self.createNewTileSet(window, fileManager, tileBox),\
                    Gtk.Label("Static"))
            notebook.append_page(self.createNewAnimation(window, fileManager, tileBox),\
	                Gtk.Label("Animation"))

            window.connect("destroy", self.quitWindow, window, "cancel")
            window.add(notebook)
            window.show_all()

    def createNewTileSet(self, window, fileManager, tileBox):
        accelGroup = Gtk.AccelGroup()
        window.add_accel_group(accelGroup)

        grid = Gtk.Grid()
        vgrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        vgrid.add(grid)

        path = Gtk.Label("Path")
        size =  Gtk.Label("Tile size")
        spacing = Gtk.Label("Space between tiles")
        grid.attach(path, 0, 0, 1, 1)
        grid.attach_next_to(size, path, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(spacing, size, Gtk.PositionType.BOTTOM, 1, 1)

        imageEntered = Gtk.Entry()
        imageEntered.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_FILE)
        imageEntered.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)
        imageEntered.connect("icon-press", self.openImage, fileManager)
        grid.attach_next_to(imageEntered, path, Gtk.PositionType.RIGHT, 3, 1)

        xLabel = Gtk.Label("x")
        spinTileLeft = Gtk.SpinButton()
        adjustment1 = Gtk.Adjustment(32, 0, 1000, 1, 10, 0)
        spinTileLeft.set_adjustment(adjustment1)
        adjustment2 = Gtk.Adjustment(32, 0, 1000, 1, 10, 0)
        spinTileRight = Gtk.SpinButton()
        spinTileRight.set_adjustment(adjustment2)

        xBisLabel = Gtk.Label("x")
        spinSpaceLeft = Gtk.SpinButton()
        adjustment3 = Gtk.Adjustment(32, 0, 1000, 1, 10, 0)
        spinSpaceLeft.set_adjustment(adjustment3)
        adjustment4 = Gtk.Adjustment(32, 0, 1000, 1, 10, 0)
        spinSpaceRight = Gtk.SpinButton()
        spinSpaceRight.set_adjustment(adjustment4)

        grid.attach_next_to(spinTileLeft, size, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(xLabel, spinTileLeft, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(spinTileRight, xLabel, Gtk.PositionType.RIGHT, 1, 1)

        grid.attach_next_to(spinSpaceLeft, spacing, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(xBisLabel, spinSpaceLeft, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(spinSpaceRight, xBisLabel, Gtk.PositionType.RIGHT, 1, 1)
        hbox = Gtk.Box()
        okButton = Gtk.Button(label="OK")
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_Return, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_KP_Enter, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.connect("clicked", self.newTileSet, \
        {'hTileSize':spinTileLeft, 'vTileSize':spinTileRight, \
        'hTileSpace':spinSpaceLeft, 'vTileSpace':spinSpaceRight, \
        'imageEntered':imageEntered, 'fileManager':fileManager, \
                'tileBox':tileBox, 'window':window})
        cancelButton = Gtk.Button(label="Cancel")
        cancelButton.connect("clicked", self.quitWindow, window)
        cancelButton.add_accelerator("activate", accelGroup, Gdk.KEY_Escape, 0, \
                Gtk.AccelFlags.MASK)

        hbox.pack_start(cancelButton, False, False, 0)
        hbox.pack_start(okButton, False, False, 0)
        vgrid.add(hbox)
        hbox.set_halign(Gtk.Align.END)
        hbox.set_valign(Gtk.Align.END)

        return vgrid

    def newTrace(self, widget, traceManager):
        if globalVar.sfmlArea:
            window = Gtk.Window()
            window.set_property("modal", True)
            notebook = Gtk.Notebook()
            notebook.append_page(self.createNewStaticTrace(window, traceManager),\
                    Gtk.Label("Static"))
            notebook.append_page(self.createNewDynamicTrace(window, traceManager),\
                    Gtk.Label("Dynamic"))

            window.connect("destroy", self.quitWindow, window, "cancel")
            window.add(notebook)
            window.show_all()

    def createNewDynamicTrace(self, window, traceManager):
        grid = Gtk.Grid()
        vgrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        vgrid.add(grid)
        vgrid.add(hbox)

        nameLabel = Gtk.Label("Name")
        nameEntered = Gtk.Entry(text="Trace #"+str(traceManager.getNumberOfTraces()))

        grid.attach(nameLabel, 0, 0, 1, 1)
        grid.attach_next_to(nameEntered, nameLabel, Gtk.PositionType.RIGHT, 2, 1)
        widgets = dict()
        widgets['nameEntered'] = nameEntered
        widgets['window'] = window
        widgets['traceManager'] = traceManager

        okButton = Gtk.Button(label="OK")
        cancelButton = Gtk.Button(label="Cancel")

        okButton.connect("clicked", self.newDynamicTrace, widgets)
        cancelButton.connect("clicked", self.quitWindow, window)

        hbox.pack_start(okButton, False, False, 0)
        hbox.pack_start(cancelButton, False, False, 0)
        hbox.set_halign(Gtk.Align.END)

        return vgrid

    def createNewStaticTrace(self, window, traceManager):
        accelGroup = Gtk.AccelGroup()
        window.add_accel_group(accelGroup)

        grid = Gtk.Grid()
        vgrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        vgrid.add(grid)
        nameLabel = Gtk.Label("Name")
        nameEntered = Gtk.Entry(text="Trace #"+str(traceManager.getNumberOfTraces()))

        sizeLabel = Gtk.Label("Size")
        xSizeSpinAdjustment = Gtk.Adjustment(32, 0, 100, 1, 10, 0)
        ySizeSpinAdjustment = Gtk.Adjustment(32, 0, 100, 1, 10, 0)

        xSizeSpinButton = Gtk.SpinButton()
        xSizeSpinButton.set_adjustment(xSizeSpinAdjustment)
        ySizeSpinButton = Gtk.SpinButton()
        ySizeSpinButton.set_adjustment(ySizeSpinAdjustment)

        shiftLabel = Gtk.Label("Shift")
        xShiftSpinAdjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        yShiftSpinAdjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)

        xShiftSpinButton = Gtk.SpinButton()
        xShiftSpinButton.set_adjustment(xShiftSpinAdjustment)
        yShiftSpinButton = Gtk.SpinButton()
        yShiftSpinButton.set_adjustment(yShiftSpinAdjustment)

        xSizeLabel = Gtk.Label("x")
        xShiftLabel = Gtk.Label("x")

        grid.attach(nameLabel, 0, 0, 1, 1)
        grid.attach_next_to(nameEntered, nameLabel, Gtk.PositionType.RIGHT, 3, 1)
        grid.attach_next_to(sizeLabel, nameLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(xSizeSpinButton, sizeLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(xSizeLabel, xSizeSpinButton, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(ySizeSpinButton, xSizeLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(shiftLabel, sizeLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(xShiftSpinButton, shiftLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(xShiftLabel, xShiftSpinButton, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(yShiftSpinButton, xShiftLabel, Gtk.PositionType.RIGHT, 1, 1)

        hbox = Gtk.Box()
        okButton = Gtk.Button(label="OK")
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_Return, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_KP_Enter, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.connect("clicked", self.newStaticTrace, \
                {'xSizeSpinButton':xSizeSpinButton, 'ySizeSpinButton':ySizeSpinButton,\
                'nameEntered':nameEntered, 'xShiftSpinButton':xShiftSpinButton,\
                'yShiftSpinButton':yShiftSpinButton, 'traceManager':traceManager, 'window':window})
        cancelButton = Gtk.Button(label="Cancel")
        cancelButton.connect("clicked", self.quitWindow, window)
        cancelButton.add_accelerator("activate", accelGroup, Gdk.KEY_Escape, 0, \
                Gtk.AccelFlags.MASK)

        hbox.pack_start(cancelButton, False, False, 0)
        hbox.pack_start(okButton, False, False, 0)
        vgrid.add(hbox)

        hbox.set_halign(Gtk.Align.END)
        hbox.set_valign(Gtk.Align.END)

        return vgrid

    def newTileSet(self, button, widgets):
        spacing = sf.Vector2(0, 0)
        if 'hTileSize' and 'vTileSpace' in widgets:
            spacing = sf.Vector2(widgets['hTileSpace'].get_value(), widgets['vTileSpace'].get_value())

        widgets['tileBox'].cutTileSet(widgets['imageEntered'].get_text(), \
            sf.Vector2(widgets['hTileSize'].get_value(), widgets['vTileSize'].get_value()), \
            spacing)	
        if 'window' in widgets:
            widgets['window'].destroy()

    def createNewAnimation(self, window, fileManager, tileBox):
        accelGroup = Gtk.AccelGroup()
        window.add_accel_group(accelGroup)
        grid = Gtk.Grid()
        vgrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        vgrid.add(grid)

        widgets = dict()
        widgets['imageWindow'] = window

        fileLabel = Gtk.Label("File")

        imageEntered = Gtk.Entry()
        imageEntered.set_icon_from_stock(Gtk.EntryIconPosition.SECONDARY, Gtk.STOCK_FILE)
        imageEntered.set_icon_activatable(Gtk.EntryIconPosition.SECONDARY, True)
        imageEntered.connect("icon-press", self.openImage, fileManager)
        grid.attach(fileLabel, 0, 0, 1, 1)
        grid.attach_next_to(imageEntered, fileLabel, Gtk.PositionType.RIGHT, 3, 1)
        widgets['imageEntered'] = imageEntered

        hbox = Gtk.Box()

        setDynamicTableSize = Gtk.Button(label="Set Dynamic Table")
        setDynamicTableSize.connect("clicked", self.setDynamicTable, widgets)
        hbox.pack_start(setDynamicTableSize, False, False, 0)

        setStaticTableSize = Gtk.Button(label="Set Static Table")
        setStaticTableSize.connect("clicked", self.setStaticTable, widgets)
        hbox.pack_start(setStaticTableSize, False, False, 0)

        box = Gtk.Box()
        okButton = Gtk.Button(label="OK")
        okButton.connect("clicked", self.cutAnimation, widgets)
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_Return, 0, \
                Gtk.AccelFlags.VISIBLE)
        okButton.add_accelerator("activate", accelGroup, Gdk.KEY_KP_Enter, 0, \
                Gtk.AccelFlags.VISIBLE)

        cancelButton = Gtk.Button(label="Cancel")
        cancelButton.connect("clicked", self.quitWindow, window)
        cancelButton.add_accelerator("activate", accelGroup, Gdk.KEY_Escape, 0, \
                Gtk.AccelFlags.MASK)
        box.pack_start(cancelButton, False, False, 0)
        box.pack_start(okButton, False, False, 0)
        box.set_halign(Gtk.Align.END)
        hbox.pack_start(box, True, True, 0)

        vgrid.add(hbox)
        return vgrid

    def newDynamicTable(self):
        treeScore = Gtk.TreeStore(str, str, str, str, str)
        treeView = Gtk.TreeView(model=treeScore)

        titleRenderer = Gtk.CellRendererText()
        posXRenderer= Gtk.CellRendererText() 
        posYRenderer= Gtk.CellRendererText() 
        sizeXRenderer= Gtk.CellRendererText() 
        sizeYRenderer= Gtk.CellRendererText() 

        columnTitle = Gtk.TreeViewColumn("Name", titleRenderer, text=0)
        columnPosX = Gtk.TreeViewColumn("Position x", posXRenderer, text=1)
        columnPosY = Gtk.TreeViewColumn("Position y", posYRenderer, text=2)
        columnSizeX = Gtk.TreeViewColumn("Size x", sizeXRenderer, text=3)
        columnSizeY = Gtk.TreeViewColumn("Size y", sizeYRenderer, text=4)

        treeView.append_column(columnTitle)
        treeView.append_column(columnPosX)
        treeView.append_column(columnPosY)
        treeView.append_column(columnSizeX)
        treeView.append_column(columnSizeY)

        return treeView

    def newStaticTable(self):
        treeScore = Gtk.TreeStore(str, str, str, str, str, str, str, str, str)
        treeView = Gtk.TreeView(model=treeScore)

        titleRenderer = Gtk.CellRendererText()
        nRenderer     = Gtk.CellRendererText()
        nXRenderer    = Gtk.CellRendererText()
        posXRenderer  = Gtk.CellRendererText()
        posYRenderer  = Gtk.CellRendererText()
        spacXRenderer = Gtk.CellRendererText()
        spacYRenderer = Gtk.CellRendererText()
        sizeXRenderer = Gtk.CellRendererText()
        sizeYRenderer = Gtk.CellRendererText()

        columnTitle   = Gtk.TreeViewColumn("Name", titleRenderer, text = 0)
        columnN       = Gtk.TreeViewColumn("Number of Tiles", nRenderer, text=1)
        columnNX      = Gtk.TreeViewColumn("Tile on X", nXRenderer, text = 2)
        columnPosX    = Gtk.TreeViewColumn("Position x", posXRenderer, text = 3)
        columnPosY    = Gtk.TreeViewColumn("Position y", posYRenderer, text = 4)
        columnSpacX   = Gtk.TreeViewColumn("Spacing x", spacXRenderer, text = 5)
        columnSpacY   = Gtk.TreeViewColumn("Spacing y", spacYRenderer, text = 6)
        columnSizeX   = Gtk.TreeViewColumn("Tile size x", sizeXRenderer, text = 7)
        columnSizeY   = Gtk.TreeViewColumn("Tile size y", sizeYRenderer, text = 8)

        treeView.append_column(columnTitle)
        treeView.append_column(columnN)
        treeView.append_column(columnNX)
        treeView.append_column(columnPosX)
        treeView.append_column(columnPosY)
        treeView.append_column(columnSpacX)
        treeView.append_column(columnSpacY)
        treeView.append_column(columnSizeX)
        treeView.append_column(columnSizeY)

        return treeView

    def setStaticTable(self, button, widgets):
        if not widgets['imageEntered'].get_text():
            return
        if 'static' in widgets:
            if widgets['static']['imageEntered'] is not widgets['imageEntered']:
                widgetsDynamic = widgets['static']
                for key in widgetsDynamic.keys():
                    if key != "imageEntered":
                        del widgetsDynamic[key]
                del widgets['static']

        if not 'static' in widgets:
            widgets['static'] = dict()

        staticWidgets = widgets['static']
        staticWidgets['imageEntered'] = widgets['imageEntered']

        window = Gtk.Window(title="New image")
        staticWidgets['table'] = self.newStaticTable()
        if not 'treeCopied' in staticWidgets:
            staticWidgets['treeStore'] = staticWidgets['table'].get_model()

        staticWidgets['table'].set_model(staticWidgets['treeStore'])
        treeCopy = functions.copyTreeStore(staticWidgets['table'].get_model())
        staticWidgets['treeCopied'] = treeCopy
        staticWidgets['window'] = window

        hBox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        hBox.pack_start(staticWidgets['table'], True, True, 0)
        hBox.pack_start(self.insertNewStaticAnimation(staticWidgets), False, False, 0)

        vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vBox.pack_start(hBox, True, True, 0)
        vBox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)
        vBox.pack_start(self.actionAnimation(staticWidgets), False, False, 0)

        window.set_property("modal",True)
        window.connect('delete-event', self.cancelAnimation, staticWidgets)
        window.add(vBox)
        window.show_all()

    def setDynamicTable(self, button, widgets):
        if not widgets['imageEntered'].get_text():
            return

        if 'dynamic' in widgets:
            if widgets['dynamic']['imageEntered'] is not widgets['imageEntered']:
                widgetsDynamic = widgets['dynamic']
                for key in widgetsDynamic.keys():
                    if key != "imageEntered":
                        del widgetsDynamic[key]
                del widgets['dynamic']

        if not 'dynamic' in widgets:
            widgets['dynamic'] = dict()

        dynamicWidgets = widgets['dynamic']
        dynamicWidgets['imageEntered'] = widgets['imageEntered']
        dynamicWidgets['table'] = self.newDynamicTable()

        window = Gtk.Window(title="New image")

        if not 'treeCopied' in dynamicWidgets:
            dynamicWidgets['treeStore'] = dynamicWidgets['table'].get_model()

        dynamicWidgets['table'].set_model(dynamicWidgets['treeStore'])
        treeCopy = functions.copyTreeStore(dynamicWidgets['table'].get_model())
        dynamicWidgets['treeCopied'] = treeCopy
        dynamicWidgets['window'] = window

        hBox = Gtk.Box(spacing=6,orientation=Gtk.Orientation.HORIZONTAL)
        hBox.pack_start(dynamicWidgets['table'], True, True, 0)
        hBox.pack_start(self.insertNewDynamicAnimation(dynamicWidgets), False, False, 0)

        vBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vBox.pack_start(hBox, True, True, 0)
        vBox.pack_start(Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL), False, False, 0)
        vBox.pack_start(self.actionAnimation(dynamicWidgets), False, False, 0)

        window.set_property("modal",True)
        window.connect('delete-event', self.cancelAnimation, dynamicWidgets)
        window.add(vBox)
        window.show_all()

    def insertNewStaticAnimation(self, widgets):
        if not widgets['imageEntered'].get_text():
            return
        grid = Gtk.Grid()
        vGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        vGrid.add(grid)
        vGrid.add(hbox)

        imagePixbuf         = GdkPixbuf.Pixbuf.new_from_file(widgets['imageEntered'].get_text())
        nameLabel           = Gtk.Label("Name")
        nLabel              = Gtk.Label("Number of Tiles")
        nXLabel             = Gtk.Label("Tiles per rows")

        titleLabel          = Gtk.Label()
        xLabel              = Gtk.Label("Position X")
        yLabel              = Gtk.Label("Position Y")
        spacXLabel          = Gtk.Label("Spacing X")
        spacYLabel          = Gtk.Label("Spacing Y")
        sizeXLabel          = Gtk.Label("Tile Size X")
        sizeYLabel          = Gtk.Label("Tile Size Y")

        nameEntry           = Gtk.Entry()
        nAdjustment         = Gtk.Adjustment(1, 1, imagePixbuf.get_width(), 1, 10, 0)
        nXAdjustment        = Gtk.Adjustment(1, 1, imagePixbuf.get_width(), 1, 10, 0)
        positionXAdjustment = Gtk.Adjustment(0, 0, imagePixbuf.get_width(), 1, 10, 0)
        positionYAdjustment = Gtk.Adjustment(0, 0, imagePixbuf.get_height(), 1, 10, 0)

        spacXAdjustment     = Gtk.Adjustment(0, 0, imagePixbuf.get_width(), 1, 10, 0)
        spacYAdjustment     = Gtk.Adjustment(0, 0, imagePixbuf.get_height(), 1, 10, 0)

        sizeXAdjustment     = Gtk.Adjustment(1, 1, imagePixbuf.get_width(), 1, 10, 0)
        sizeYAdjustment     = Gtk.Adjustment(1, 1, imagePixbuf.get_height(), 1, 10, 0)

        nSpin               = Gtk.SpinButton(adjustment = nAdjustment)
        nXSpin              = Gtk.SpinButton(adjustment = nXAdjustment)
        xSpin               = Gtk.SpinButton(adjustment = positionXAdjustment)
        ySpin               = Gtk.SpinButton(adjustment = positionYAdjustment)
        spacXSpin           = Gtk.SpinButton(adjustment = spacXAdjustment)
        spacYSpin           = Gtk.SpinButton(adjustment = spacYAdjustment)
        sizeXSpin           = Gtk.SpinButton(adjustment = sizeXAdjustment)
        sizeYSpin           = Gtk.SpinButton(adjustment = sizeYAdjustment)

        addEntity           = Gtk.Button(label = "Add")
        resetEntity         = Gtk.Button(label = "Reset")

        separator           = Gtk.Separator(orientation = Gtk.Orientation.HORIZONTAL)

        grid.attach(nameLabel, 0,0,1,1)
        grid.attach_next_to(nameEntry, nameLabel, Gtk.PositionType.RIGHT, 1, 2)
        grid.attach_next_to(separator, nameLabel, Gtk.PositionType.BOTTOM, 3, 1)
        grid.attach_next_to(titleLabel, separator, Gtk.PositionType.BOTTOM, 4, 1)

        grid.attach_next_to(nLabel, titleLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(nSpin, nLabel, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(nXLabel, nLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(nXSpin, nXLabel, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(xLabel, nXLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(xSpin, xLabel, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(yLabel, xLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(ySpin, yLabel, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(spacXLabel, yLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(spacXSpin, spacXLabel, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(spacYLabel, spacXLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(spacYSpin, spacYLabel, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(sizeXLabel, spacYLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(sizeXSpin, sizeXLabel, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(sizeYLabel, sizeXLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(sizeYSpin, sizeYLabel, Gtk.PositionType.RIGHT, 2, 1)

        hbox.pack_start(addEntity, False, False, 0)
        hbox.pack_start(resetEntity, False, False, 0)
        hbox.set_halign(Gtk.Align.END)
        hbox.set_valign(Gtk.Align.END)


        widgets['nameAnnimEntered'] = nameEntry

        widgets['n'] = nSpin
        widgets['nX'] = nXSpin
        widgets['positionX'] = xSpin
        widgets['positionY'] = ySpin
        widgets['spacX'] = spacXSpin
        widgets['spacY'] = spacYSpin
        widgets['sizeX'] = sizeXSpin
        widgets['sizeY'] = sizeYSpin

        addEntity.connect('clicked', self.addStaticEntityInTree, widgets)
        resetEntity.connect('clicked', self.resetEntity, widgets)

        return vGrid

    def insertNewDynamicAnimation(self, widgets):
        if not widgets['imageEntered'].get_text():
            return
        grid = Gtk.Grid()
        vGrid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        vGrid.add(grid)
        vGrid.add(hbox)

        imagePixbuf = GdkPixbuf.Pixbuf.new_from_file(widgets['imageEntered'].get_text())
        nameLabel = Gtk.Label("Name")

        titleLabel = Gtk.Label()
        xLabel = Gtk.Label("Position X")
        yLabel = Gtk.Label("Position Y")
        sizeXLabel = Gtk.Label("Size X")
        sizeYLabel = Gtk.Label("Size Y")

        nameEntry = Gtk.Entry()
        positionXAdjustment = Gtk.Adjustment(0, 0, imagePixbuf.get_width(), 1, 10, 0) 
        positionYAdjustment = Gtk.Adjustment(0, 0, imagePixbuf.get_height(), 1, 10, 0) 
        sizeXAdjustment = Gtk.Adjustment(1, 1, imagePixbuf.get_width(), 1, 10, 0) 
        sizeYAdjustment = Gtk.Adjustment(1, 1, imagePixbuf.get_height(), 1, 10, 0) 
        xSpin = Gtk.SpinButton(adjustment=positionXAdjustment)
        ySpin = Gtk.SpinButton(adjustment=positionYAdjustment)
        sizeXSpin = Gtk.SpinButton(adjustment=sizeXAdjustment)
        sizeYSpin = Gtk.SpinButton(adjustment=sizeYAdjustment)

        addAnnim = Gtk.Button(label="Add")
        addEntity = Gtk.Button(label="Add")
        resetEntity = Gtk.Button(label="Reset")

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        grid.attach(nameLabel, 0,0,1,1)
        grid.attach_next_to(nameEntry, nameLabel, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(addAnnim, nameEntry, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(separator, nameLabel, Gtk.PositionType.BOTTOM, 3, 1)
        grid.attach_next_to(titleLabel, separator, Gtk.PositionType.BOTTOM, 4, 1)
        grid.attach_next_to(xLabel, titleLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(xSpin, xLabel, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(yLabel, xLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(ySpin, yLabel, Gtk.PositionType.RIGHT, 2, 1)

        grid.attach_next_to(sizeXLabel, yLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(sizeXSpin, sizeXLabel, Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(sizeYLabel, sizeXLabel, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(sizeYSpin, sizeYLabel, Gtk.PositionType.RIGHT, 2, 1)

        hbox.pack_start(addEntity, False, False, 0)
        hbox.pack_start(resetEntity, False, False, 0)
        hbox.set_halign(Gtk.Align.END)
        hbox.set_valign(Gtk.Align.END)


        widgets['nameAnnimEntered'] = nameEntry

        widgets['positionX'] = xSpin
        widgets['positionY'] = ySpin
        widgets['sizeX'] = sizeXSpin
        widgets['sizeY'] = sizeYSpin

        addAnnim.connect('clicked', self.addAnniInTree, widgets)
        addEntity.connect('clicked', self.addDynamicEntityInTree, widgets)
        resetEntity.connect('clicked', self.resetEntity, widgets)

        return vGrid

    def addAnniInTree(self, button, widgets):
        parent=widgets['treeStore'].append(None)
        widgets['treeStore'].set_value(parent, 0, widgets['nameAnnimEntered'].get_text())

    def addStaticEntityInTree(self, button, widgets):
        name = widgets['nameAnnimEntered'].get_text()
        if name == "":
            return

        parent = widgets['treeStore'].append(None, row = [name,\
                str(int(widgets['n'].get_value())),\
                str(int(widgets['nX'].get_value())),\
                str(int(widgets['positionX'].get_value())),\
                str(int(widgets['positionY'].get_value())),\
                str(int(widgets['spacX'].get_value())),\
                str(int(widgets['spacY'].get_value())),\
                str(int(widgets['sizeX'].get_value())),\
                str(int(widgets['sizeY'].get_value()))])

    def addDynamicEntityInTree(self, button, widgets):
        if len(widgets['treeStore']) == 0:
            return
        parent = widgets['table'].get_selection().get_selected()[1]
        if not parent:
            parent = widgets['treeStore'].get_iter(len(widgets['treeStore']) - 1)

        name=0

        while widgets['treeStore'].iter_parent(parent):
            name += widgets['treeStore'].iter_n_children(parent)
            parent = widgets['treeStore'].iter_parent(parent)

        widgets['treeStore'].insert_with_values(parent, -1, range(5), \
                [name + widgets['treeStore'].iter_n_children(parent),\
                str(int(widgets['positionX'].get_value())),\
                str(int(widgets['positionY'].get_value())),\
                str(int(widgets['sizeX'].get_value())),\
                str(int(widgets['sizeY'].get_value()))])

    def resetEntity(self, button, widgets):
        widgets['positionX'].set_value(widgets['positionX'].get_adjustment().get_lower())
        widgets['positionY'].set_value(widgets['positionY'].get_adjustment().get_lower())
        widgets['sizeX'].set_value(widgets['sizeX'].get_lower())
        widgets['sizeY'].set_value(widgets['sizeY'].get_lower())

    def cutAnimation(self, button, widgets):
        dynamicTable = None
        staticTable = None
        imageEntered = widgets['imageEntered'].get_text()

        if 'dynamic' in widgets:
            dynamicWidgets = widgets['dynamic']
            if 'table' in dynamicWidgets:
                dynamicTable = dynamicWidgets['treeStore']

        if 'static' in widgets:
            staticWidgets = widgets['static']
            if 'table' in staticWidgets:
                staticTable = staticWidgets['treeStore']

            self.parent.tileBox.cutAnimationTreeStore(dynamicTable, staticTable, imageEntered)

        self.quitWindow(button, widgets['imageWindow'])

    def actionAnimation(self, widgets):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        actionBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        delBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        actionBox.set_halign(Gtk.Align.END)
        actionBox.set_valign(Gtk.Align.END)
        delBox.set_valign(Gtk.Align.END)
        delBox.set_halign(Gtk.Align.START)
        box.set_valign(Gtk.Align.END)

        box.pack_start(delBox, False, False, 0)
        box.pack_start(actionBox, False, False, 0)

        okButton = Gtk.Button(label="OK")
        cancelButton = Gtk.Button(label="Cancel")
        applyButton = Gtk.Button(label="Apply")

        clearAll = Gtk.Button(label="Clear")
        clearAll.connect('clicked', lambda b, treeStore : treeStore.clear(), widgets['treeStore'])
        delete = Gtk.Button(label="Delete")
        delete.connect('clicked', self.deleteEntryInTreeStore, widgets)

        delBox.pack_start(delete, False, False, 0)
        delBox.pack_start(clearAll, False, False, 0)

        actionBox.pack_start(applyButton, False, False, 0)
        actionBox.pack_start(okButton, False, False, 0)
        actionBox.pack_start(cancelButton, False, False, 0)

        cancelButton.connect('clicked', self.cancelAnimation, None, widgets)
        okButton.connect('clicked', self.quitWindow, widgets['window'])
        applyButton.connect('clicked', self.copieTreeStore, widgets)

        return box

    def deleteEntryInTreeStore(self, button, widgets):
        parent = widgets['table'].get_selection().get_selected()[1]
        if not parent:
            return
        widgets['treeStore'].remove(parent)

    def copieTreeStore(self, button, widgets):
        widgets['treeCopied'] = functions.copyTreeStore(widgets['treeStore'])

    def cancelAnimation(self, button, event, widgets):
        widgets['treeStore'] = widgets['treeCopied']
        self.quitWindow(button, widgets['window'])

    def newStaticTrace(self, button, widgets):
        widgets['traceManager'].addStaticTrace(sf.Vector2(int(widgets['xSizeSpinButton'].get_value()),\
            int(widgets['ySizeSpinButton'].get_value())),\
            sf.Vector2(int(widgets['xShiftSpinButton'].get_value()),\
            int(widgets['yShiftSpinButton'].get_value())),\
            widgets['nameEntered'].get_text())
        if 'window' in widgets:
            widgets['window'].destroy()

    def newDynamicTrace(self, button, widgets):
        widgets['traceManager'].addDynamicTrace(widgets['nameEntered'].get_text())
        if 'window' in widgets:
            widgets['window'].destroy()

    def setSize(self):
        return

    def quitWindow(self, *args, **kwargs):
        args[1].destroy()

    def openImage(self, entry, pos, event, fileManager):
        path = fileManager.openFileImage()
        if path:
            entry.set_text(path)

    def initNewFile(self, button, widgets):
        addString = ''
        if widgets['nameEntered'].get_text()[-4:] != ".xml":
            addString = ".xml"

        globalVar.tileWindow.buildSFMLArea(sf.Vector2(\
                int(widgets["hNumberCases"].get_value()), int(widgets["vNumberCases"].get_value())),\
                sf.Vector2(\
				int(widgets["hTileSize"].get_value()), int(widgets["vTileSize"].get_value())))

        globalVar.sfmlArea.get_toplevel().set_title(\
                widgets['nameEntered'].get_text().replace(".xml", ""))
        globalVar.tileWindow.fileManager.xmlFile = 'Files/'+globalVar.tileWindow.get_title()+'.xml'
        window = widgets['window']
        del widgets['window']
        window.destroy()
