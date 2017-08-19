#-*- coding: utf-8 -*-
from openerp import api, fields, models, _

class SurveySurvey(models.Model):
    _inherit = ['survey.survey']
    x_product_ids = fields.Many2many('product.product',
                                         string='Survey')
    
class ProjectProject(models.Model):
    _inherit = ['project.project']
    x_survey_id = fields.Many2one('survey.survey',string='Encuesta')
    
class ProjectTask(models.Model):
    _inherit = ['project.task']
    x_survey_id = fields.Many2one('survey.survey',string='Encuesta')
    x_recursive = fields.Boolean('Recursive?')
    x_create_source = fields.Boolean('Create Source ?')
    survey_user_input_ids = fields.Many2many('survey.user_input',string='Respuesta')
    
class SurveyUserInput(models.Model):
    _inherit = ['survey.user_input']
    x_product_ids = fields.Many2one('product.product')
    project_task_ids = fields.Many2many('project.task')
    
class SurveyUserInputLine(models.Model):
    _inherit = ['survey.user_input_line']
    x_state = fields.Selection([
        ('skip','skip'),
        ('done','done')],
        'Priority',default='skip')
    

class ProjectTaskType(models.Model):
    _inherit = ['project.task.type']
    x_task_type = fields.Selection([
        ('0','IN PREPARATION'),
        ('1','PENDING'),
        ('2','ON FIELD'),
        ('3','RETURNED FROM FIELD'),
        ('4','CANCEL'),
        ('5','OTHER')],
        'Priority',default='5')    
    