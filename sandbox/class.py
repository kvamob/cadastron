from area import Area

class Arealoc:
    name = 'Test'

    def print_name(self, n):
        self.name = n
        print(n)
    pass


if __name__ == '__main__':
    area_l = Arealoc()
    print(area_l.name)
    area_l.print_name('11111111111')
    print(area_l.name)

#    area = Area()
 #   print(area.cadaster)
  #  print(area.name)


