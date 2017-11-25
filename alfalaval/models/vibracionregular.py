# -*- coding: utf-8 -*-

from odoo import models, fields, api

class vibracionregular(models.Model):
     _name = 'vibracionregular'
     
     cliente = fields.Char(string='Datos del cliente',size=12,required=True,help='Registrar el cliente')
     codigocliente = fields.Char(string='Código del cliente',required=True,help='Registrar el código del cliente')
     numeroos = fields.Integer(string='OS No',required=True,size=10,help='Registrar el número de OS')
     equipo = fields.Char(string='Equipo',size=12,required=True,help='Registrar el equipo')
     prodn = fields.Char(string='Prod No',size=12,required=True,help='Registrar el Prod No')
     flujo = fields.Char(string='Flujo m3/h',size=12,required=True,help='Registrar el flujo m3/h')
     precision = fields.Char(string='Precisión',size=12,required=True,help='Registrar la precisión')
     image = fields.Binary('Image')
     
     #Mediciones Regulares
     #vacio mm
     mrvaciomm1 = fields.Char(string='Medición regular 1 En vacío .mm/s',size=12,help='Medición regular 1 En vacío .mm/s')
     mrvaciomm2 = fields.Char(string='Medición regular 2 En vacío .mm/s',size=12,help='Medición regular 2 En vacío .mm/s')
     mrvaciomm3 = fields.Char(string='Medición regular 3 En vacío .mm/s',size=12,help='Medición regular 3 En vacío .mm/s')
     mrvaciomm4 = fields.Char(string='Medición regular 4 En vacío .mm/s',size=12,help='Medición regular 4 En vacío .mm/s')
     mrvaciomm5 = fields.Char(string='Medición regular 5 En vacío .mm/s',size=12,help='Medición regular 5 En vacío .mm/s')
     mrvaciomm6 = fields.Char(string='Medición regular 6 En vacío .mm/s',size=12,help='Medición regular 6 En vacío .mm/s')
     
     #vacio gE
     mrvacioge1 = fields.Char(string='Medición regular 1 En vacío .gE',size=12,help='Medición regular 1 En vacío .gE')
     mrvacioge2 = fields.Char(string='Medición regular 2 En vacío .gE',size=12,help='Medición regular 2 En vacío .gE')
     mrvacioge3 = fields.Char(string='Medición regular 3 En vacío .gE',size=12,help='Medición regular 3 En vacío .gE')
     mrvacioge4 = fields.Char(string='Medición regular 4 En vacío .gE',size=12,help='Medición regular 4 En vacío .gE')
     mrvacioge5 = fields.Char(string='Medición regular 5 En vacío .gE',size=12,help='Medición regular 5 En vacío .gE')
     mrvacioge6 = fields.Char(string='Medición regular 6 En vacío .gE',size=12,help='Medición regular 6 En vacío .gE')
     
    #agua mm
     mraguamm1 = fields.Char(string='Medición regular 1 En agua .mm/s',size=12,help='Medición regular 1 En agua .mm/s')
     mraguamm2 = fields.Char(string='Medición regular 2 En agua .mm/s',size=12,help='Medición regular 2 En agua .mm/s')
     mraguamm3 = fields.Char(string='Medición regular 3 En agua .mm/s',size=12,help='Medición regular 3 En agua .mm/s')
     mraguamm4 = fields.Char(string='Medición regular 4 En agua .mm/s',size=12,help='Medición regular 4 En agua .mm/s')
     mraguamm5 = fields.Char(string='Medición regular 5 En agua .mm/s',size=12,help='Medición regular 5 En agua .mm/s')
     mraguamm6 = fields.Char(string='Medición regular 6 En agua .mm/s',size=12,help='Medición regular 6 En agua .mm/s')
     
     #agua gE
     mraguage1 = fields.Char(string='Medición regular 1 En agua .gE',size=12,help='Medición regular 1 En agua .gE')
     mraguage2 = fields.Char(string='Medición regular 2 En agua .gE',size=12,help='Medición regular 2 En agua .gE')
     mraguage3 = fields.Char(string='Medición regular 3 En agua .gE',size=12,help='Medición regular 3 En agua .gE')
     mraguage4 = fields.Char(string='Medición regular 4 En agua .gE',size=12,help='Medición regular 4 En agua .gE')
     mraguage5 = fields.Char(string='Medición regular 5 En agua .gE',size=12,help='Medición regular 5 En agua .gE')
     mraguage6 = fields.Char(string='Medición regular 6 En agua .gE',size=12,help='Medición regular 6 En agua .gE')
    
    #carga mm
     mrcargamm1 = fields.Char(string='Medición regular 1 En carga .mm/s',size=12,help='Medición regular 1 En carga .mm/s')
     mrcargamm2 = fields.Char(string='Medición regular 2 En carga .mm/s',size=12,help='Medición regular 2 En carga .mm/s')
     mrcargamm3 = fields.Char(string='Medición regular 3 En carga .mm/s',size=12,help='Medición regular 3 En carga .mm/s')
     mrcargamm4 = fields.Char(string='Medición regular 4 En carga .mm/s',size=12,help='Medición regular 4 En carga .mm/s')
     mrcargamm5 = fields.Char(string='Medición regular 5 En carga .mm/s',size=12,help='Medición regular 5 En carga .mm/s')
     mrcargamm6 = fields.Char(string='Medición regular 6 En carga .mm/s',size=12,help='Medición regular 6 En carga .mm/s')
     
     #carga gE
     mrcargage1= fields.Char(string='Medición regular 1 En carga .gE',size=12,help='Medición regular 1 En carga .gE')
     mrcargage2= fields.Char(string='Medición regular 2 En carga .gE',size=12,help='Medición regular 2 En carga .gE')
     mrcargage3= fields.Char(string='Medición regular 3 En carga .gE',size=12,help='Medición regular 3 En carga .gE')
     mrcargage4= fields.Char(string='Medición regular 4 En carga .gE',size=12,help='Medición regular 4 En carga .gE')
     mrcargage5= fields.Char(string='Medición regular 5 En carga .gE',size=12,help='Medición regular 5 En carga .gE')
     mrcargage6= fields.Char(string='Medición regular 6 En carga .gE',size=12,help='Medición regular 6 En carga .gE')
    
    
     
     observacion = fields.Text(string='Observación',help='Observación')
     valormaximo = fields.Char(string='Valor máximo medido en mm/s',required=True,help='Valor máximo medido en mm/s')
     
     firmafieldservice = fields.Binary('Field Service Manager')
     firmacliente = fields.Binary('Cliente')
     
    

     @api.depends('value')
     def _value_pc(self):
         self.value2 = float(self.value) / 100