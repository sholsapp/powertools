import inspect


def tree(node, _depth=1):
  """Print a tree.

  Sometimes it's useful to print datastructures as a tree. This function prints
  out a pretty tree with root `node`. A tree is represented as a :class:`dict`,
  whose keys are node names and values are :class:`dict` objects for sub-trees
  and :class:`None` for terminals.

  :param node: The root of the tree to print.

  """
  current = 0
  length = len(node.keys())
  tee_joint = '\xe2\x94\x9c\xe2\x94\x80\xe2\x94\x80'
  elbow_joint = '\xe2\x94\x94\xe2\x94\x80\xe2\x94\x80'
  for key, value in node.iteritems():
    current += 1
    if current == length:
       yield ' {space} {key}'.format(space=elbow_joint, key=key)
    else:
       yield ' {space} {key}'.format(space=tee_joint, key=key)
    if value:
      for e in tree(value, _depth=_depth + 1):
        yield (' |  ' if current != length else '    ') + e


def treeable(clz):
  """Convert a class instance to a tree-able object.

  :param clz: The class instance to convert to a :func:`tree`-able
    :class:`dict` object.

  """
  tree = {}
  for name, attr in inspect.getmembers(clz):
    if not name.startswith('__') and not inspect.isbuiltin(attr):
      if isinstance(attr, object) and not any(isinstance(attr, t) for t in [str, int, float, list, dict]):
        tree[name] = to_dict_tree(getattr(clz, name))
      else:
        tree[name] = {attr: None}
  return tree
