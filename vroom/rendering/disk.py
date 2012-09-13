def disk(radius, **kwargs):
   quadric = _get_quadric()
   texture = kwargs.get('texture', None)
   style = kwargs.get('style', 'wireframe')
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   else:
      gluQuadricTexture(quadric, False)
   _set_draw_style(style)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   if texture:
      texture.unbind()

