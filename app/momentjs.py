from jinja2 import Markup

class momentjs(object):
    def __init__(self, timestamp, locale='ru'):
        self.timestamp = timestamp
        self.locale = locale

    def render(self, format):
        return Markup("<script>\nmoment.lang(\"%s\");\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.locale, self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
