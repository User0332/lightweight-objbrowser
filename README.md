# Light ObjBrowser

A very light, small library that uses `tkinter` to view Python dictionaries like `console.dir` would show on a JavaScript object. If you want to log any object's properties, not just a dict's, use `browse(obj.__dict__)`, and if you want methods and properties to show, use a dictionary containing both obj's dict and its class's dict as well. ObjBrowser does *not* show properties that start with an underscore.
