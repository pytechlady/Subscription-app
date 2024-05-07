import graphene
from graphene_django import DjangoObjectType
from core.models import Company, Subscription
from core.utils import Util
from decimal import Decimal


class CompanyType(DjangoObjectType):
    class Meta:
        model = Company
        fields = "__all__"
        

class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = "__all__"
    
        
class Query(graphene.ObjectType):
    
    
    list_company = graphene.List(CompanyType)
    read_company = graphene.Field(CompanyType, company_identifier = graphene.String())
    list_subscription = graphene.List(SubscriptionType)
    list_company_subscription = graphene.List(SubscriptionType, company_name = graphene.String())
    
    def resolve_list_company(root, info):
        return Company.objects.all()
    
    def resolve_read_company(root, info, company_identifier):
        return Company.objects.get(company_identifier=company_identifier)
    
    def resolve_list_subscription(root, info):
        return Subscription.objects.all()
    
    def resolve_list_company_subscription(root, info, company_name):
        company_instance = Company.objects.get(company_identifier=company_name)
        subscriptions =Subscription.objects.filter(company_name=company_instance)
        return subscriptions
    

class CompanyMutation(graphene.Mutation):
    class Arguments:
        company_name = graphene.String()
        company_identifier = graphene.String()
        email = graphene.String()
        
    company = graphene.Field(CompanyType)
    
    def mutate(root, info, company_name, email, company_identifier=None):
        try:
            # Update an existing company
            get_company = Company.objects.get(company_identifier=company_identifier)
            get_company.company_name=company_name
            get_company.email=email
            get_company.save()
            return CompanyMutation(company=get_company)
        except Company.DoesNotExist:
            # Create a new company
            company_identifier = Util.generate_identifiers()
            company = Company(company_name=company_name, email=email, company_identifier=company_identifier)
            company.save()
            return CompanyMutation(company=company)
        

class CompanyDelete(graphene.Mutation):
    class Arguments:
        company_identifier = graphene.String()
        
    company = graphene.Field(CompanyType)
    
    def mutate(root, info, company_identifier):
        company = Company.objects.get(company_identifier=company_identifier)
        company.delete()
        
        
class SubscriptionMutation(graphene.Mutation):
    class Arguments:
        subscription_name = graphene.String()
        company_name = graphene.String()
        amount = graphene.String()
        
    subscription = graphene.Field(SubscriptionType)
    
    def mutate(root, info, subscription_name, amount, company_name):
        company_instance = Company.objects.get(company_identifier=company_name)
        try:
            amount_decimal = Decimal(amount)
            get_sub = Subscription.objects.get(subscription_name=subscription_name, company_name=company_instance)
            get_sub.amount = amount_decimal
            get_sub.subscription_name = subscription_name
            get_sub.save()
            return SubscriptionMutation(subscription=get_sub)
        
        except Subscription.DoesNotExist:
            subscription = Subscription(subscription_name=subscription_name, company_name=company_instance, amount=amount)
            subscription.save()
            return SubscriptionMutation(subscription=subscription)
        

class SubscriptionDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        # company_name = graphene.String()
        
    subscription = graphene.Field(SubscriptionType)
    
    def mutate(root, info, id):
        # print(id)
        # print(company_name)
        subscription = Subscription.objects.get(id=id)
        subscription.delete()           
       
class Mutation(graphene.ObjectType):
    create_company = CompanyMutation.Field()
    update_company = CompanyMutation.Field()
    delete_company = CompanyDelete.Field()
    create_subscription = SubscriptionMutation.Field()
    update_subscription = SubscriptionMutation.Field()
    delete_subscription = SubscriptionDelete.Field()
        

schema = graphene.Schema(query=Query, mutation=Mutation)
        