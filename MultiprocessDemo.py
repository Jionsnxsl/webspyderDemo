"""
多进程练习
"""

# import multiprocessing
# import time
#
#
# def process(num):
#     time.sleep(num)
#     print("Process:", num)
#
#
# if __name__ == '__main__':
#     for i in range(5):
#         p = multiprocessing.Process(target=process, args=(i,))
#         p.start()
#
#     print("CPU number：" + str(multiprocessing.cpu_count()))
#     for p in multiprocessing.active_children():
#         print("child process name: " + p.name + "  id: " + str(p.pid))
#
#     print("Process End")


# from multiprocessing import Pool
# import time
#
#
# def myFunc(index):
#     print("start process :", index)
#     time.sleep(3)
#     print("End process :", index)

if __name__ == "__main__":
    # pool = Pool(processes=3)
    # for i in range(4):
    #     pool.apply(myFunc, (i, ))
    #
    # print("Process Started")
    # pool.close()
    # pool.join()
    # print("subprocess done")
