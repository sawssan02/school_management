# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Grade(models.Model):
    _name = 'school.grade'
    _description = 'Note'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    # Relations
    student_id = fields.Many2one('school.student', string='Étudiant', required=True, tracking=True)
    course_id = fields.Many2one('school.course', string='Cours', required=True, tracking=True)
    
    # Informations sur la note
    grade = fields.Float(string='Note', required=True, tracking=True)
    max_grade = fields.Float(string='Note maximale', default=20.0, required=True)
    
    # Type d'évaluation
    evaluation_type = fields.Selection([
        ('homework', 'Devoir'),
        ('quiz', 'Interrogation'),
        ('midterm', 'Examen partiel'),
        ('final', 'Examen final'),
        ('project', 'Projet'),
        ('presentation', 'Présentation'),
        ('participation', 'Participation'),
    ], string="Type d'évaluation", required=True, tracking=True)
    
    # Date et période
    date = fields.Date(string='Date', default=fields.Date.today, required=True, tracking=True)
    semester = fields.Selection([
        ('1', 'Semestre 1'),
        ('2', 'Semestre 2'),
    ], string='Semestre', required=True)
    
    # Calculs
    percentage = fields.Float(string='Pourcentage', compute='_compute_percentage', store=True)
    grade_letter = fields.Selection([
        ('a+', 'A+ (Excellent)'),
        ('a', 'A (Très bien)'),
        ('b+', 'B+ (Bien)'),
        ('b', 'B (Assez bien)'),
        ('c+', 'C+ (Passable)'),
        ('c', 'C (Moyen)'),
        ('d', 'D (Insuffisant)'),
        ('f', 'F (Échec)'),
    ], string='Lettre', compute='_compute_grade_letter', store=True)
    
    # Remarques
    remarks = fields.Text(string='Remarques')
    
    # Enseignant qui a noté
    graded_by = fields.Many2one('school.teacher', string='Noté par', default=lambda self: self._get_default_teacher())
    
    @api.depends('grade', 'max_grade')
    def _compute_percentage(self):
        for record in self:
            if record.max_grade > 0:
                record.percentage = (record.grade / record.max_grade) * 100
            else:
                record.percentage = 0.0
    
    @api.depends('percentage')
    def _compute_grade_letter(self):
        for record in self:
            percentage = record.percentage
            if percentage >= 95:
                record.grade_letter = 'a+'
            elif percentage >= 90:
                record.grade_letter = 'a'
            elif percentage >= 85:
                record.grade_letter = 'b+'
            elif percentage >= 80:
                record.grade_letter = 'b'
            elif percentage >= 75:
                record.grade_letter = 'c+'
            elif percentage >= 70:
                record.grade_letter = 'c'
            elif percentage >= 60:
                record.grade_letter = 'd'
            else:
                record.grade_letter = 'f'
    
    def _get_default_teacher(self):
        # Retourne l'enseignant du cours si disponible
        return False
    
    @api.constrains('grade', 'max_grade')
    def _check_grade(self):
        for record in self:
            if record.grade < 0:
                raise ValidationError(_("La note ne peut pas être négative."))
            if record.grade > record.max_grade:
                raise ValidationError(_("La note ne peut pas dépasser la note maximale."))
            if record.max_grade <= 0:
                raise ValidationError(_("La note maximale doit être supérieure à 0."))
