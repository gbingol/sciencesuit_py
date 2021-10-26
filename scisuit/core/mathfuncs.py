
def Copy_CallObjectMethod(entry, methodName:str, *args):
      """
      Do not directly use this function. <br>
      It is used by abs, cos, cosh,..., tan, tanh math functions. <br>
      <br>

      entry: a copyable entry (must have a copy method) <br>
      methodName: entry must have a method with methodName <br>
      args: Parameters that methodName takes <br>

      for example: to call the method compute of entry v (=v.compute(10)) <br>
      CallMethod(v, "compute", 10)
      """

      EntryCopy=None
      if(hasattr(entry, "copy")):
            copyfunc=getattr(entry, "copy")

            EntryCopy=copyfunc()

      else:
            raise AttributeError("Entry is not copyable")


      if(hasattr(EntryCopy, methodName)):
            func=getattr(EntryCopy, methodName)

            if(len(args)>0):
                  func(*args)
            else:
                  func()
      else:
            raise AttributeError("Entry does not have a method: "+ methodName)

      return EntryCopy