# -*- coding: utf-8 -*-

from odoo import models, fields, api

class enel100k(models.Model):
     _name = 'enel100k.enel100k'
     
     suministro = fields.Char(string='No. Suministro',size=12,required=True,help='Registrar el numero de suministro')
     nombres = fields.Char(string='Nombres',required=True,help='Registrar los nombres')
     apellido_paterno = fields.Char(string='Apellido Paterno',required=True,help='Registrar el apellido paterno')
     apellido_materno = fields.Char(string='Apellido Materno',required=True,help='Registrar el apellido materno')
     dni = fields.Char(string='No. DNI',required=True,size=8,help='Registrar el DNI')
     telefono_fijo = fields.Char(string='Teléfono fijo',size=7,required=True,help='Registrar el teléfono fijo')
     telefono_celular = fields.Char(string='Teléfono celular',size=9,required=True,help='Registrar el teléfono celular')
     email = fields.Char(string='Correo electrónico',required=True,help='Registrar el correo electrónico')
     edad = fields.Integer(string='Edad',required=True,size=2,help='Registrar la edad')
     distrito = fields.Char(string='Distrito',required=True,help='Registrar el distrito de residencia')
     direccion = fields.Char(string='Dirección residencial',required=True,help='Registrar la dirección residencial')
     image = fields.Binary('Image')
     
    
     #value = fields.Integer()
     #value2 = fields.Float(compute="_value_pc", store=True)
     #description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
         self.value2 = float(self.value) / 100