#-*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError



class Tag(models.Model):
    _name = 'todo.task.tag'
    name = fields.Char('Name', size=40, translate=True)
    
    #Tag class relación a Tasks:
    task_ids = fields.Many2many('todo.task', # modelo relacionado
                                 string='Tasks')
    _parent_store = True
    #_parent_name  = 'parent_id'
    parent_id     = fields.Many2one('todo.task.tag','Parent Tag', ondelete='restrict')
    parent_left   = fields.Integer('Parent Left', index=True)
    parent_right  = fields.Integer('Parent  Right', index=True)
    child_ids = fields.One2many('todo.task.tag', 'parent_id', 'Child Tags')

class Stage(models.Model):
    _name  = 'todo.task.stage'
    _order = 'sequence,name'

    # Campos de cadena de caracteres:
    name  = fields.Char('Name',size=40)
    desc  = fields.Text('Description')
    state = fields.Selection([('draft','New'),('open','Started'), ('done','Closed')],'State')
    docs  = fields.Html('Documentation')

    # Campos numéricos:
    sequence      = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete',(3,2))

    # Campos de fecha:
    date_effective = fields.Date('Effective Date')
    date_changed   = fields.Datetime('Last Changed')

    # Otros campos:
    fold  = fields.Boolean('Folded?')
    image = fields.Binary('Image')
    
    #Stage class relación con Tasks:
    tasks = fields.One2many('todo.task',# modelo relacionado
                            'stage_id',# campo para "este" en el modelo relacionado
                            'Tasks in this stage')
    
class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
    refers_to = fields.Reference([('res.user', 'User'),('res.partner', 'Partner')], 'Refers to')
    stage_state = fields.Selection(related='stage_id.state', string='Stage State')
    effort_estimate = fields.Integer('Effort Estimate')
    user_todo_count  = fields.Integer('User Count')
    
    _sql_constraints = [
        ('todo_task_name_uniq',
         'UNIQUE (name, user_id, active)',
         'Task title must be unique!')]
    
    
    stage_fold = fields.Boolean
    string   = 'Stage Folded?',
    compute  ='_compute_stage_fold',
            # store=False) # predeterminado
    #search   ='_search_stage_fold',
    inverse  ='_write_stage_fold'
    
    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold
        
    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold
        
    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) < 5:
             raise ValidationError('Must have 5 chars!')
    
    @api.one 
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)])
        user_todo_count = fields.Integer('User To-Do   Count', compute='compute_user_todo_count')
    
    
