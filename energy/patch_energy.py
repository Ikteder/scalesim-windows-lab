"""Repair memory-capacity conversion and the OFMAP repeated-access source."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from patch_scalesim import patch
import patch_scalesim
patch_scalesim.FIXES=[
 ('rundir-accelergy/preprocess.py','SramSz = int(SramSz) * 1024\n',
  'SramSz = int(SramSz) * 1024 // (4 * MemoryBanks)\n'),
 ('scalesim/energy/accelergy_plugin.py',
  'self.ofmap_sram_repeat = self.sram_repeat_check(bank_size=self.SRAM_bank_size, memory = memory_system.ifmap_trace_matrix, row_size=self.SRAM_row_size)',
  'self.ofmap_sram_repeat = self.sram_repeat_check(bank_size=self.SRAM_bank_size, memory = memory_system.ofmap_trace_matrix, row_size=self.SRAM_row_size)')]
if __name__=='__main__':patch(Path.cwd())
