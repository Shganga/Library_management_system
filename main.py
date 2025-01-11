from GUI import *
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='library_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    root = tk.Tk()
    app = GUI(root,logging)
    root.mainloop()