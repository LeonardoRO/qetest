from qetest.src.tests.nova.batchtest import BatchTest
from qetest.src.tests.nova.panelmenu.renametest import PanelRenameTest
from qetest.src.tests.nova.panelmenu.tagtest import PanelTagTest
from qetest.src.tests.nova.panelmenu.colortest import PanelColorTest
from qetest.src.tests.nova.panelmenu.powertest import PanelPowerTest
from qetest.src.tests.nova.panelmenu.passwordtest import PanelPasswordTest
from qetest.src.tests.nova.panelmenu.rebuildtest import PanelRebuildTest
from qetest.src.tests.nova.panelmenu.resizetest import PanelResizeTest
from qetest.src.tests.nova.panelmenu.imagetest import PanelCreateImageTest
from qetest.src.tests.nova.addservertest import AddServerTest

__all__ = ['ALL_TEST_KLASSES',]

ALL_TEST_KLASSES = [
                    BatchTest,
                    PanelRenameTest,
                    PanelTagTest,
                    PanelColorTest,
                    PanelPowerTest,
                    PanelPasswordTest,
                    PanelRebuildTest,
                    PanelResizeTest,
                    PanelCreateImageTest,
                    AddServerTest,
                    ]
