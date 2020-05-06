import xml.etree.ElementTree as xml
import uuid

class CardParse(object):
    data = {}
    qs = []
    actionqs = []
    xml = xml.Element("main")
    act = xml.Element('Action')
    problems = xml.Element('Problem')

    def __init__(self, *args, **kwargs):
        self.actionqs = kwargs['action']
        self.xml.append(self.act)
        self.xml.append(self.problems)
        actid = xml.SubElement(self.act, "id")
        actid.text = str(self.actionqs.pk)
        actname = xml.SubElement(self.act, "name")
        actname.text = str(self.actionqs.act)
        actarg = xml.SubElement(self.act, "arg")
        actarg.text = str(self.actionqs.arg)


    def update(self, data):
        id = xml.Element(data['nomdobr'])
        self.xml.append(id)
        newstatus = xml.SubElement(id, 'newstatus')
        newstatus.text = data['status']
        laststatus = xml.SubElement(id, 'laststatus')
        success = xml.SubElement(id, 'success')
        if Problem.objects.filter(nomdobr=data['nomdobr']).exists():
            prob = Problem.objects.get(nomdobr=data['nomdobr'])
            laststatus.text = prob.status
            prob.temat = data['temat']
            prob.podcat = data['podcat']
            prob.text = data['text']
            prob.adres = data['adres']
            prob.datecre = data['datecre']
            prob.dateotv = data['dateotv']
            prob.status = data['status']
            prob.parsing = data['parsing']
            prob.visible = data['visible']
        else:
            prob = Problem(nomdobr=data['nomdobr'], temat=data['temat'], podcat=data['podcat'], text=data['text'],
                           adres=data['adres'], datecre=data['datecre'], status=data['status'], parsing=data['parsing'],
                           dateotv=data['dateotv'], visible=data['visible'])
        prob.save()
        prob = Problem.objects.get(nomdobr=data['nomdobr'])
        if prob.status == data['status']:
            success.text = 'Successfully'
        else:
            success.text = 'Unsuccessfully'

    def close(self):
        path = MEDIA_ROOT + 'cardpas/'
        fn = f'act-{self.actionqs.pk}.xml'
        tree = xml.ElementTree(self.xml)
        with open(path + fn, 'wb') as fh:
            tree.write(fh)
