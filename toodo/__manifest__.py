# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'todoo',
    'author' : 'MYR Consultoria en Sistemas SAC',
    'depends' : ['project','survey','contacts','project_task_code','base_action_rule'],
    'category' : 'Project',
    'application' : True,
    'website': 'http://www.myrconsulting.net',
    'data': [
        'views/todo_view_survey.xml',
        'views/todo_view_project_project.xml',
        'views/todo_view_project_task.xml',
        'views/todo_view_survey_user_input.xml',
        'security/todo_access_rules.xml',
        'data/project_task_type.xml',
        #'data/ir_actions_server.xml',
        #'data/base_action_rule.xml',
        'data/ir_ui_menu.xml'
        
    ],
    'installable'    :   True,
    'auto_install'  :   True,
    'active'    :   True
}