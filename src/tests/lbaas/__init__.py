from qetest.src.tests.lbaas.listviewtest import ListViewTest
from qetest.src.tests.lbaas.detailsviewtest import DetailViewTest
from qetest.src.tests.lbaas.renametest import RenameTest
#from qetest.src.tests.lbaas.algorithmtest import AlgorithmTest
#from qetest.src.tests.lbaas.protocolporttest import ProtocolPortTest

__all__ = ['ALL_TEST_KLASSES',]

ALL_TEST_KLASSES = [
    ListViewTest,
    DetailViewTest,
    RenameTest,
#    AlgorithmTest,
#    ProtocolPortTest,
    ]