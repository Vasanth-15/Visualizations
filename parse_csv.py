import csv
import argparse
import math
from itertools import product
'''
  Enum for all possible commands w.r.t column index
  Assumptions
  - Timestamp will be always at starting column 
  - create enum for one PC and update TOTAL col per pc
  - Cols will repeat across PCs 
'''
class CMD:
  CYCLE = 0
  ACT = 1
  RDREQ = 2 #Writes need to be added
  REF = 3
  TOTAL = 3

class BankActivityPlot:
  def __init__(self, args):
    self._pc = args.num_pc
    self._bank = args.num_bank
    self._rank = args.num_rank
    self._csvfile = args.input_file
    self._y = ["PC"+str(pc)+"_Bank"+str(bank)+"_Rank"+str(rank) for pc, rank, bank in \
              product(range(self._pc), range(self._rank), range(self._bank))]
    self._data = {
      "read_x": [],
      "read_y": [],
      "write_x": [],
      "write_y": [],
      "act_x": [],
      "act_y": [],
      "ref_x": [],
      "ref_y": []
    }
    self.__read_csv_build_dt()

  '''
    Add property decorator to set class member variables
  '''
  # @property
  # def pc(self):
  #   return self._pc

  # @pc.setter
  # def pc(self, value):
  #   self._pc = value

  def plot(self):
    print(self._data)

  # __ implies this function is private


  def __read_csv_build_dt(self):
    with open(self._csvfile, 'r') as file:
      csvreader = csv.reader(file)
      for line in csvreader:
        line = list(filter(None, line))
        cycle = line[CMD.CYCLE] #TBD: convert to cycles
        for pc_id in range(self._pc):
          act = line[CMD.ACT + pc_id*CMD.TOTAL]
          self.__update_dt(act, CMD.ACT, pc_id, cycle)

          rdreq = line[CMD.RDREQ + pc_id*CMD.TOTAL]
          self.__update_dt(rdreq, CMD.RDREQ, pc_id, cycle)          

          # wrreq = line[CMD.WRREQ + pc_id*CMD.TOTAL]
          # __update_dt(wrreq, CMD.WRREQ, pc_id, cycle)

          ref = line[CMD.REF + pc_id*CMD.TOTAL]
          self.__update_dt(ref, CMD.REF, pc_id, cycle)


  def __update_dt(self, cmd, cmd_type, pc_id, cycle):
    '''
      We are assuming that the datastructure is built as below
      First we plot banks followed by rank and then PC
      index = Bank_number + (PC_number*number_of_ranks + Rank_number)*number_of_banks
    '''
    cal_idx = lambda bank_id, rank_id: bank_id + \
              (pc_id*self._rank + rank_id)*self._bank

    bank_id = self.__hget_bank_id(cmd)
    if bank_id != -1:
      y_idx = int(cal_idx(bank_id, 0)) # hardcoding rank to 0
      y_idx = self._y[y_idx]
      # check for command type and update x and y coordinates
      if cmd_type == CMD.ACT:
        self._data["act_y"].append(y_idx)
        self._data["act_x"].append(cycle)
      elif cmd_type == CMD.RDREQ:
        self._data["read_y"].append(y_idx)
        self._data["read_x"].append(cycle)
      # elif cmd_type == CMD.WRREQ:
      #   self._data["write_y"].append(y_idx)
      #   self._data["write_x"].append(cycle)
      elif cmd_type == CMD.REF:
        self._data["ref_y"].append(y_idx)
        self._data["ref_x"].append(cycle)  

  def __hget_bank_id(self, cmd):
    '''
      Assuming cmd has hex string
    '''
    i_cmd = int(cmd,16)
    idx = -1
    if i_cmd > 0:
      idx = math.log(i_cmd, 2)
    return idx


if __name__ == "__main__":
  #your user inputs goes here
  parser = argparse.ArgumentParser()
  parser.add_argument('--csv', dest='input_file', help="Pass the csv file dumped from fsdb", required=True)
  parser.add_argument('--pcs', dest='num_pc', default=2, help="Number of pcs")
  parser.add_argument('--banks', dest='num_bank', default=16, help="Number of banks")
  parser.add_argument('--ranks', dest='num_rank', default=1, help="Number of ranks")

  args = parser.parse_args()
  #lets parse csv and plot dram bank activity
  bplot = BankActivityPlot(args)
  bplot.plot()
