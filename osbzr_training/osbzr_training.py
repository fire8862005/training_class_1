# -*- encoding: utf-8 -*-
from  odoo  import  models,fields,api,exceptions
class training_subject(models.Model):
    _name = 'training.subject'
    _rec_name = 'name'

    name = fields.Char(u'名称',
                        size=64,
                        required=True)

    manager_id = fields.Many2one(string= u'负责人',
                        comodel_name='res.users')

    lesson_ids = fields.One2many(comodel_name='training.lesson',inverse_name='subject_id',string='课程')

    description = fields.Text('描述')

    @api.multi
    def name_get(self):
        res = super(training_subject,self).name_get()
        result =[]
        if self.env.context.get("form"):
            for index, name in res:
                subject = self.browse(index)
                result.append((index,name + "-%s" % subject.manager_id.name or ""))
            return result
        else:
            return res

class training_lesson(models.Model):
    _name = 'training.lesson'
    _rec_name = 'name'

    name = fields.Char(u'名称',
                        size=64,
                        required=True)

    subject_id = fields.Many2one(string= u'科目名称',
                        comodel_name='training.subject')

    start_date = fields.Date("开始日期")
    end_date = fields.Date("结束日期")
    sites = fields.Integer("座位数")
    state = fields.Selection([("new",u'招生'),("start",u'已开课'),("end",u'结束')],string ="状态",default ="new")
    teacher_id = fields.Many2one(comodel_name='res.partner',string="老师",domain="[('is_teacher','=',True)]")
    student_ids = fields.Many2many(comodel_name='res.partner', string="学生")
    _sql_constraints = [
        ('uniq_name','unique(name)','课程名必须唯一'),
    ]
    @api.constrains('end_date','start_date')
    def check_date(self):
        for lesson in self :
            if lesson.end_date <lesson.start_date :
                raise exceptions.ValidationError(u'开始日期不能大于结束日期')

    @api.constrains('sites')
    def check_lesson(self):
        for lesson in self :
            if lesson.sites <0 :
                raise exceptions.ValidationError(u'坐席数不能为零')

    @api.multi
    def start(self):
        for lesson in self :
            self.state ="start"

    @api.multi
    def end(self):
        for lesson in self :
            self.state ="end"

class res_partner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _is_teacher(self):
        return self.env.context.get('teacher')

    is_teacher=fields.Boolean(u'是老师',default =_is_teacher)