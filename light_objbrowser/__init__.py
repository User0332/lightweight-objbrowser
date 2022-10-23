import tkinter as tk
import tkinter.ttk as widgets

def _traverse(obj: dict[str], tree: widgets.Treeview, parent_id="obj"):
	i = 0
	for key, value in obj.items():
		if key.startswith('_'): continue
		_id = f"{parent_id}['{key}']"
		tree.insert(parent_id, i, _id, text=key)

		if type(value) is dict:
			_traverse(value, tree, parent_id=_id)

			i+=1
			continue

		if type(value) is list:
			for j, item in enumerate(value):
				key_id = f"{_id}[{j}]"
				tree.insert(_id, j, key_id, text=j)
				if type(item) is dict:
					_traverse(item, tree, key_id)
					continue

				tree.insert(key_id, 0, f"{key_id} value", text=item)
				
			i+=1
			continue

		tree.insert(_id, 0, f"{_id} value", text=repr(value))

		i+=1

def browse(obj: dict, objname="object", name="Object Browser", height=500, width=1000):
	root = tk.Tk()
	root.title(name)
	root.geometry(f"{width}x{height}")
	root.resizable(True, True)

	tree = gettreeobj(obj, root, objname, height, width)
	
	tree.pack()

	root.mainloop()

def gettreeobj(obj: dict, root:tk.Tk, objname="object", height=500, width=1000):
	tree = widgets.Treeview(
		root,
		height=height,
		columns="col1",
		selectmode="browse"
	)

	tree.bind(
		"<Return>", 
		lambda e: [ # this basically creates a new
			browse( # window for the selected object(s)
				eval(
					_id, 
					{ "obj": obj }
				)
				if type(
					eval(
						_id, 
						{ "obj": obj }
					)
				) is dict else
				{
					str(i): item
					for i, item in 
					enumerate(
						eval(
							_id, 
							{ "obj": obj }
						)
					)
				},
				tree.item(_id)["text"],
				name=root.title(),
				height=height,
				width=width
			)

			for _id in tree.selection()
			if not _id.endswith("value") and 
			type(
				eval(
					_id, 
					{ "obj": obj }
				)
			) in (list, dict)
		]
	) 
	# geez - these lambdas get huge
	# and have a lot of repeat code!
	# (and are really unreadable)


	tree.insert('', 0, "obj", text=objname)
	
	_traverse(obj, tree)

	tree.column(
		"col1",
		minwidth=0,
		width=width,
		stretch=tk.YES
	)

	return tree