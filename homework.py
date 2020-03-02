class Tag:
    def __init__(self, tagname, is_single=False, klass=None, **kwargs):
        self.text=""
        self.attributes={}
        self.tagname=tagname
        self.is_single=is_single
        self.attributes={}
        self.html_code=[];

        if klass is not None:
            self.attributes["class"]=" ".join(klass)

        for attr, value in kwargs.items():
            self.attributes[attr]=value

    def __enter__(self):
        attrs=[]
        if self.attributes:
            for attr, value in self.attributes.items():
                attrs.append('%s = "%s"' % (attr,value))
        attrs=" ".join(attrs)
        if attrs:
            attrs=" "+attrs
        end_tag_symbol=""
        if self.is_single:
            end_tag_symbol="/"

        self.html_code.append("<{tag}{attr}{endsym}>".format(tag=self.tagname, attr=attrs, endsym=end_tag_symbol))
        
        return self
    def __exit__(self, type, value, traceback):
        pass

    def __add__(self, other):
        if hasattr(other,"text") and other.text!="":  
            other.html_code.append(other.text)
        if not other.is_single:
            other.html_code.append("</{}>".format(other.tagname))
        self.html_code+=other.html_code
        return self

    
    
class HTML(Tag):
    def __init__(self, output):
        self.tagname="html"
        self.output=output
        self.toplevel=True
        self.attributes={}
        self.is_single=False;
        self.html_code=[]

    def __exit__(self, type, value, traceback):
            self.html_code.append("</{}>".format(self.tagname))
            self.outputResult()

    def outputResult(self):
        str_val="\n".join(self.html_code);
        if self.output is None:
            print(str_val)
            return
        with open(self.output, "w") as f: 
            f.write(str_val)

class TopLevelTag(Tag):
    pass



if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                    div += img

                body += div

            doc += body
