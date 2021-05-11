from text_proc import proc_doc, proc_query

class File:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        self.proc =  proc_doc(title) + proc_doc(body)

    def __str__(self):
        return f'id: {self.id} \ntitle: {self.title} \nbody: {self.body}'

class Query:
    def __init__(self, id, body):
        self.id = id
        self.body = body
        self.proc = proc_query(body)

    def __str__(self):
        return f'id: {self.id} \nbody: {self.body}'