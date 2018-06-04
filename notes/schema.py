from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import Note as NoteModel

class Note(DjangoObjectType):
    class Meta:
        model = NoteModel

        # this line is a boileplate line that identifies this data as a node in the graph database.
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    notes = graphene.List(Note)

    def resolve_notes(self, info):
        user = info.context.user

        if settings.DEBUG:
            return NoteModel.objects.all()
        elif user.is_anonymous:
            return NoteModel.objects.none()
        else:
            return NoteModel.objects.filter(user=user)


# adding a schema to attach to the query for GraphQL
schema = graphene.Schema(query=Query)
            