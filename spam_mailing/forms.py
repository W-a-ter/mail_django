from django.forms import ModelForm

from spam_mailing.models import Mailing, Message, Receiver


class ReceiverForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReceiverForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите email получателя"})
        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите ФИО получателя"})
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Дополнительная информация"}
        )

    class Meta:
        model = Receiver
        fields = "__all__"


class MessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields["text_topic"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему письма"})
        self.fields["text_body"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})

    class Meta:
        model = Message
        fields = "__all__"


class MailingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields["date_start"].widget.attrs.update({"class": "form-control", "placeholder": "Введите тему письма"})
        self.fields["date_end"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})
        self.fields["status"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})
        self.fields["text_msg"].widget.attrs.update({"class": "form-control", "placeholder": "Введите текст письма"})
        self.fields["receivers_msgs"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите текст письма"}
        )

    class Meta:
        model = Mailing
        fields = "__all__"
