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

NONE = 'NA'
CA = 'CA'
WA = 'WA'
STATE_CHOISES = (
    (NONE, '--'),
    (CA, 'California'),
    (WA, 'Washington'),
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
    # Required fields
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True)
    uid = models.CharField(max_length=16, unique=True)
    
    # Basic info
    first_name = models.CharField(max_length=16, blank=True)
    last_name = models.CharField(max_length=16, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    # Gender
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


    # Location
    residence_city = models.CharField(max_length=32, blank=True)
    residence_state = models.CharField(max_length=2,
                                       choices=STATE_CHOISES,
                                       default=NONE)

    # Misc.
    bio = models.CharField(max_length=160, blank=True)
    contacts = models.ManyToManyField('self', 
                                      through='Relationship',
                                      symmetrical=False, 
                                      related_name='related_to')


    # Job fields
    job_title = models.CharField(max_length=32, blank=True)
    job_employer = models.CharField(max_length=32, blank=True)

    # Permissions
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


    def create_relationship(self, contact, address, symm=True, **kwargs):
        relationship, create = Relationship.objects.get_or_create(from_user=self,
                                                          to_user=contact)
#                                                          address=address)
        relationship.address = address
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
            if not pair_relationship.address:
                pair_relationship.address = address
            pair_relationship.save()
        return relationship

    def remove_relationship(self, contact, status, symm=True):
        Relationship.objects.filter(
                                    from_user=self,
                                    to_user=contact,
                                    status=status).delete()
        if symm:
            contact.remove_relationship(self, status, False)

    def get_relationships(self):
        return Relationship.objects.filter(from_user=self,
                                           status=RELATIONSHIP_ACCPTED)
    def get_pending_relationships(self):
        return Relationship.objects.filter(to_user=self,
                                           status=RELATIONSHIP_PENDING)

#class Location(models.Model):
#    name = models.CharField(max_length=128, blank=True)
#    address = models.CharField(max_length=256, blank=True)
#    latitude = models.DecimalField(max_digits=6, decimal_places=3)
#    longitude = models.DecimalField(max_digits=6, decimal_places=3)

#    def __unicode__(self):
#        return "Location"
    
class Relationship(models.Model):
    to_user = models.ForeignKey(UserProfile, related_name='from_users')
    from_user = models.ForeignKey(UserProfile, related_name='to_users')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES,
                                 default=RELATIONSHIP_PENDING)
    date_requested = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=256, blank=True)
    
#    location = models.ForeignKey(Location, related_name='location')
    
    class Meta:
        verbose_name = _('relationship')
        verbose_name_plural = _('relationships')
 
    def __str__(self):
        return "Contact request from " + self.from_user.email + " to " + self.to_user.email


