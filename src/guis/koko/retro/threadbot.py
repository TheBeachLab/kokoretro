import subprocess

import koko.retro.globals
from   koko.retro.render import RenderTask
from   koko.retro.export import ExportTask, FabTask

class ThreadBot(object):
    ''' Threadbot keeps track of threads running various tasks.
        It may hold multiple render threads, up to one export thread,
        and up to one fab thread.

        It also keeps track of the current cad structure.
    '''

    def __init__(self):
        self.cached_cad     = None
        self.export_task    = None
        self.fab_task       = None
        self.tasks = []

    def render(self, view, shapes=[], script=''):
        ''' Begins a new render task. '''

        self.stop_threads()
        self.join_threads()

        # Save a copy of the view
        view = view.copy()

        if not shapes and not script:
            self.tasks += [RenderTask(view, cad=self.cached_cad)]
        else:
            self.tasks += [RenderTask(view, shapes=shapes, script=script)]


    def glrender(self, shapes, script):
        ''' Begins a new triangulation task. '''
        self.stop_threads()
        self.join_threads()

        self.tasks += [GLRenderTask(shapes, script)]


    def export(self, path, resolution):
        ''' Begins a new export task. '''
        if '.asdf' in path:
            self.export_task = ASDFexportTask(path, self.cached_cad, resolution)
        else:
            self.export_task = ExportTask(path, self.cached_cad, resolution)


    def start_fab(self):
        ''' Starts the fab modules running. '''
        if self.cached_cad is None:
            dialogs.warning('Design needs to be succesfully rendered before opening fab modules!')
            return
        self.fab_task = FabTask(self.cached_cad)

    def reset(self):
        ''' Halts all threads and deletes cached cad data. '''
        self.cached_cad = None
        self.stop_threads()

    def stop_threads(self):
        ''' Informs each thread that it should stop. '''
        for task in self.tasks:
            task.event.set()
            task.c_event.set()


    def join_threads(self):
        ''' Joins any thread whose work is finished.

            Grabs the cad data structure from render threads, storing
            it as cached_cad (for later re-use).

            Re-writes the cad data structure to file if the fab modules
            are running in the fab_task thread.
        '''

        updated = False
        for task in self.tasks:
            if not task.thread.is_alive():
                self.cached_cad = task.cad
                updated = True
                task.thread.join()
        self.tasks = filter(lambda t: t.thread.is_alive(), self.tasks)

        if self.fab_task:
            if self.fab_task.poll() is not None:
                self.fab_task = None
            else:
                if updated:
                    self.fab_task.update(self.cached_cad)
                p = self.fab_task.load_path()
                if p is not None and koko.retro.retro.globals.GLCANVAS:
                    koko.retro.retro.globals.GLCANVAS.load_path(p)
                    koko.retro.retro.globals.GLCANVAS.Refresh()


        if self.export_task and not self.export_task.thread.is_alive():
            self.export_task.thread.join()
            self.export_task = None


