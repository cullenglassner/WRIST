from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from WRIST import settings

RELATIONSHIP_ACCPTED = 1
RELATIONSHIP_DENIED  = 2
RELATIONSHIP_PENDING = 3
RELATIONSHIP_STATUSES = (
                         (RELATIONSHIP_ACCPTED, 'Accepted'),
                         (RELATIONSHIP_DENIED, 'Denied'),
                         (RELATIONSHIP_PENDING, 'Pending'),
                         )


class UserProfileManager(BaseUserManager):
    def create_user(self, email, uid, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        if not uid:
            raise ValueError('The given UID must be set')
        uid = uid

        user = self.model(email=email, uid=uid)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, uid, password):
        user = self.create_user(email, uid, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True)
    uid = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    contacts = models.ManyToManyField('self', 
                                      through='Relationship',
                                      symmetrical=False, 
                                      related_name='related_to')
    phone_number = models.CharField(max_length=15, blank=True)
    bio = models.CharField(max_length=160, blank=True)
    NONE = 'NA'
    MALE = 'MA'
    FEMALE = 'FE'
    GENDER_CHOICES = (
                      (NONE, "None"),
                      (MALE, "Male"),
                      (FEMALE, "Female"),
                      )
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default=NONE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['uid']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    def create_relationship(self, contact, symm=True):
        relationship, create = Relationship.objects.get_or_create(from_user=self,
                                                          to_user=contact)
        try:
            pair_relationship = Relationship.objects.get(from_user=contact,
                                                         to_user=self)
        except Relationship.DoesNotExist:
            return relationship
        except Relationship.MultipleObjectsReturned:
            return pair_relationship[:1]
        if symm:
            relationship.status = RELATIONSHIP_ACCPTED  
            relationship.save()
            pair_relationship.status = RELATIONSHIP_ACCPTED
            pair_relationship.save()
        return relationship

    def remove_relationship(self, contact, status, symm=True):
        Relationship.objects.filter(
                                    from_user=self,
                                    to_user=contact,
                                    status=status).delete()
        if symm:
            contact.remove_relationship(self, status, False)

    def get_relationships(self, status):
        return Relationship.objects.filter(to_user=self,
                                           status=status)


class Relationship(models.Model):
    to_user = models.ForeignKey(UserProfile, related_name='from_users')
    from_user = models.ForeignKey(UserProfile, related_name='to_users')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES,
                                 default=RELATIONSHIP_PENDING)
    date_requested = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=1023)
    
    class Meta:
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
 
    def __str__(self):
        return "Contact request from " + self.from_user.email + " to " + self.to_user.email


