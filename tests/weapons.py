

#wapons
class WeaponBase:
	def __init__(self):
		self.attached_gadget = None
	def fire(self):
		print self.__class__.__name__, "fired:", self.rounds_per_shot
		print "sound:", self.sound
		print "speed:", self.speed
	def attach(self, gadget):
		assert self.__class__ in gadget.compatible  # TODO: better check
		self.sound = gadget.getSound(self.ammo) + "_" + self.sound_default
		self.attached_gadget = gadget
	def reload(self, ammo):
		assert self.__class__ in ammo.compatible  # TODO: better check
		if self.attached_gadget:
			self.sound = self.attached_gadget.getSound(ammo) + "_" + self.sound_default
		else:
			self.sound = ammo.getSound() + "_" + self.sound_default
		self.ammo = ammo

class ProjectileWeaponBase (WeaponBase):
	pass # TODO: refactor projectile weapon constructors here

class Pistol (ProjectileWeaponBase):
	def __init__(self, ammo):
		ProjectileWeaponBase.__init__(self) # super
		self.ammo = ammo
		self.rounds_per_shot = 1
		self.speed = 10
		self.sound_default = "pistol"
		self.sound = ammo.getSound() + "_" + self.sound_default

class Rifle (ProjectileWeaponBase):
	def __init__(self, ammo):
		ProjectileWeaponBase.__init__(self) # super
		self.ammo = ammo
		self.rounds_per_shot = 3
		self.speed = 15
		self.sound_default = "rifle"
		self.sound = ammo.getSound() + "_" + self.sound_default

# The Knife is a hack - it is both weapon and ammo
class Knife(WeaponBase):
	def __init__(self):
		WeaponBase.__init__(self) # super
		self.rounds_per_shot = 1
		self.speed = 1
		self.sound_default = "knife"
		self.sound = "knife_hiss"
		self.ammo = self
	def getSound(self):
		return "hiss"

# ammo
class AmmoBase:
	def __init__(self, q):
		self.quantity = q

class PistolHPAmmo (AmmoBase):
	compatible = [Pistol]
	def getSound(self):
		return "HP"

class PistolAPAmmo (AmmoBase):
	compatible = [Pistol]
	def getSound(self):
		return "AP"

class RifleAPAmmo (AmmoBase):
	compatible = [Rifle]
	def getSound(self):
		return "AP"

class RifleHEAmmo (AmmoBase):
	compatible = [Rifle]
	def getSound(self):
		return "HE"

# addons
class PistolSilencer:
	compatible = [Pistol]
	def getSound(self, ammo):
		return "silinced_" + ammo.getSound()

class RifleSilencer:
	compatible = [Rifle]
	def getSound(self, ammo):
		return "silinced_" + ammo.getSound()

class Poison:
	compatible = [Knife]
	def getSound(self, ammo):
		return "poisoned_" + ammo.getSound()


#main
#TODO: real tests with assertions

print "knife test"
knife = Knife()
knife.fire()
print "\npoisoned knife test"
knife.attach(Poison())
knife.fire()

print "\npistol HP test"
pistol = Pistol(PistolHPAmmo(7))
pistol.fire()
print "\npistol AP test"
pistol.reload(PistolAPAmmo(7))
pistol.fire()
print "\npistol AP silinced test"
pistol.attach(PistolSilencer())
pistol.fire()

print "\nrifle AP test"
rifle = Rifle(RifleAPAmmo(30))
rifle.fire()
print "\nrifle AP silinced test"
rifle.attach(RifleSilencer())
rifle.fire()
print "\nrifle HE test"
rifle.reload(RifleHEAmmo(30))
rifle.fire()
