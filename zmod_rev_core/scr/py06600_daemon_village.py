import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, coe_consts
import py14710_smith, py14711_smith_wife, py14712_wizard, py14713_priest, py06601_village_npc, py14714_mayor

# import py06500_daemon_barovia
# py06500_daemon_barovia.cs()
# game.fade_and_teleport(0, 0, 0, 5125, 429, 478)
# game.fade_and_teleport(0, 0, 0, 5125, 467, 478)

MAP_ID_VILLAGE = 5126
VILLAGE = "village"
VILLAGE_DAEMON_SCRIPT = 6500
VILLAGE_DAEMON_ID = "G_777CFFCC_1864_4C4D_B05F_ECE4C6EF4B18"
VILLAGE_DAEMON_DIALOG = 6600

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != MAP_ID_VILLAGE): toee.RUN_DEFAULT
	ctrl = CtrlVillage.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != MAP_ID_VILLAGE): toee.RUN_DEFAULT
	ctrl = CtrlVillage.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != MAP_ID_VILLAGE): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlVillage.ensure(attachee)
		ctrl.place_encounters(1)
	if (ctrl):
		ctrl.heartbeat()
	return toee.RUN_DEFAULT

def san_dying(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	c = cs()
	if (c):
		c.critter_dying(attachee, triggerer)
	storage = utils_storage.obj_storage_by_id(attachee.id)
	if (storage):
		cb = storage.get_data(ctrl_behaviour.CtrlBehaviour.get_name())
		if ("dying" in dir(cb)):
			cb.dying(attachee, triggerer)
	return toee.RUN_DEFAULT

def san_use(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	print("san_use id: {}, nameid: {}".format(attachee.id, attachee.name))
	if (attachee.name == coe_consts.PORTAL_KASSEN_2_ROAD_2_EVERFLAME):
		toee.game.fade_and_teleport(0, 0, 0, coe_consts.MAP_ID_ROAD2COE, 484, 458)
		return toee.SKIP_DEFAULT
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(VILLAGE_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlVillage.get_name() in o.data):
		result = o.data[CtrlVillage.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlVillage(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlVillage, self).__init__()
		return

	def created(self, npc):
		super(CtrlVillage, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = VILLAGE_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlVillage"

	@classmethod
	def get_alias(self):
		return "village" # utils_storage.ca("village")

	def get_map_default(self):
		return MAP_ID_VILLAGE

	def place_encounters(self, new_map):
		print("new_map: {}".format(new_map))
		print("place_encounters.encounters_placed == {}".format(self.encounters_placed))
		startup_zmod.zmod_templeplus_config_apply()
		startup_zmod.zmod_conditions_apply_pc()

		if (self.encounters_placed and new_map == 0): return

		this_entrance_time = toee.game.time.time_game_in_hours2(toee.game.time)
		print("this_entrance_time == {}".format(this_entrance_time))
		if (not self.encounters_placed):
			self.first_entered_shrs = this_entrance_time
		self.last_entered_shrs = this_entrance_time
		if (not self.last_leave_shrs):
			self.last_leave_shrs = this_entrance_time

		if (not self.encounters_placed):
			self.create_npc_at(utils_obj.sec2loc(478, 508), py14710_smith.CtrlVillageSmith, const_toee.rotation_0900_oclock, "merchant", "smith", None, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(476, 505), py14711_smith_wife.CtrlVillageSmithWife, const_toee.rotation_0800_oclock, "merchant", "smith_wife", None, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(503, 477), py14712_wizard.CtrlVillageWizard, const_toee.rotation_0200_oclock, "merchant", "wizard", None, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(494, 506), py14713_priest.CtrlVillagePriest, const_toee.rotation_1100_oclock, "merchant", "priest", None, 0, 1)
			self.create_npc_at(utils_obj.sec2loc(475, 475), py14714_mayor.CtrlVillageMayor, const_toee.rotation_1000_oclock, "authority", "mayor", None, 0, 1)
			self.generate_crowd()

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)

		#toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 479, 494) #smith
		toee.game.fade_and_teleport(0, 0, 0, self.get_map_default(), 466, 468) #near fontain entrance
		utils_obj.scroll_to_leader()
		return

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlVillage, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = VILLAGE_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return VILLAGE_DAEMON_DIALOG

	def get_monster_faction_default(self, npc):
		return factions_zmod.FACTION_NEUTRAL_NPC

	def generate_crowd(self):
		num = 0
		x = 464
		while (x <= 472-2):
			x += 2
			y = 468
			while (y <= 486-2):
				x1 = x + toee.game.random_range(0, 1)
				y += 2 + toee.game.random_range(0, 1)
				num += 1
				cl = py06601_village_npc.CtrlVillageManRandom
				if (toee.game.random_range(0, 1)):
					cl = py06601_village_npc.CtrlVillageWomanRandom
				self.create_npc_at(utils_obj.sec2loc(y, x1), cl, const_toee.rotation_0500_oclock, "crowd", "person_{}".format(num), None, 0, 1)
		return

	def quest_everflame_recieved(self):
		toee.game.quests[coe_consts.QUEST_EVERFLAME].state = toee.qs_accepted
		utils_storage.ca("mayor_uptal").quest_everflame_recieved()

		exit_loc = utils_obj.sec2loc(505, 473)
		objs = utils_storage.Storage().objs
		assert isinstance(objs, dict)
		m3 = copy.copy(self.m2)
		for minfo in m3:
			assert isinstance(minfo, monster_info.MonsterInfo)
			#print("minfo.name: {}, minfo.id: {}".format(minfo.name, minfo.id))
			if (minfo.name.find("crowd") != -1):
				id = minfo.id
				self.m2.remove(minfo)
				del self.monsters[minfo.name]
				del objs[id]
				#npc = minfo.get_npc()
				npc = utils_toee.get_obj_by_id(id)
				print(npc)
				assert isinstance(npc, toee.PyObjHandle)
				if (npc):
					#print("npc.runoff(), {}".format(npc))
					npc.runoff(exit_loc, 0, 0)
				#else: print("npc not found: {}, id: {}".format(npc, id))
		return

	def get_monster_prefix_default(self):
		return "village"
