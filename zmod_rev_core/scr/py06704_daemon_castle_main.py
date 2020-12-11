import toee, debug, utils_toee, utils_storage, utils_obj, utils_item, const_proto_weapon, const_proto_armor, const_toee, ctrl_daemon, const_proto_items
import ctrl_behaviour, py06122_cormyr_prompter, factions_zmod, const_proto_scrolls, const_proto_wands, utils_npc
import startup_zmod, utils_sneak, monster_info, copy, rev_consts, math, utils_locks, utils_trap, const_traps
import const_proto_containers, const_proto_list_weapons_masterwork, const_proto_potions, const_proto_wands

CASTLE_MAIN = "CASTLE_MAIN"
CASTLE_MAIN_DAEMON_SCRIPT = 6704
CASTLE_MAIN_DAEMON_ID = "G_FD116A49_8AF4_4E49_A40F_C43E0BC9DCF8"
CASTLE_MAIN_DAEMON_DIALOG = 6704

def san_new_map(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_new_map")
	if (attachee.map != rev_consts.MAP_ID_CASTLE_MAIN): toee.RUN_DEFAULT
	ctrl = CtrlCastleMain.ensure(attachee)
	ctrl.place_encounters(1)
	return toee.RUN_DEFAULT

def san_first_heartbeat(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#print(attachee.id)
	#debug.breakp("san_first_heartbeat")
	startup_zmod.zmod_templeplus_config_apply()
	if (attachee.map != rev_consts.MAP_ID_CASTLE_MAIN): toee.RUN_DEFAULT
	ctrl = CtrlCastleMain.ensure(attachee)
	ctrl.place_encounters(0)
	return toee.RUN_DEFAULT

def san_heartbeat_disable(attachee, triggerer):
	assert isinstance(attachee, toee.PyObjHandle)
	#debug.breakp("san_heartbeat")
	if (attachee.map != rev_consts.MAP_ID_CASTLE_MAIN): toee.RUN_DEFAULT
	startup_zmod.zmod_templeplus_config_apply()
	ctrl = cs()
	if (not ctrl):
		ctrl = CtrlCastleMain.ensure(attachee)
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
	if (attachee.name == rev_consts.PORTAL_CASTLE_MAIN_2_CASTLE_COURT):
		#toee.game.fade_and_teleport(0, 0, 0, rev_consts.MAP_ID_ROAD2COE, 468, 507)
		return toee.SKIP_DEFAULT
	return toee.RUN_DEFAULT

def cs():
	#print("CtrlShatteredLab.get_name(): {}".format(CtrlShatteredLab.get_name()))
	o = utils_storage.obj_storage_by_id(CASTLE_MAIN_DAEMON_ID)
	#print("utils_storage.obj_storage(): {}".format(o))
	if (not o): return None
	if (CtrlCastleMain.get_name() in o.data):
		result = o.data[CtrlCastleMain.get_name()]
	else: return None
	#print("data: {}".format(result))
	#debugg.breakp("csl")
	return result

class CtrlCastleMain(ctrl_daemon.CtrlDaemon):
	def __init__(self):
		super(CtrlCastleMain, self).__init__()
		return

	def created(self, npc):
		super(CtrlCastleMain, self).created(npc)
		npc.scripts[const_toee.sn_dialog] = CASTLE_MAIN_DAEMON_SCRIPT
		return

	@staticmethod
	def get_name():
		return "CtrlCastleMain"

	@classmethod
	def get_alias(self):
		return "CASTLE_MAIN" # utils_storage.ca("CASTLE_MAIN")

	def get_map_default(self):
		return rev_consts.MAP_ID_CASTLE_MAIN

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
			pass

		self.encounters_placed += 1
		self.factions_existance_refresh()
		self.check_sleep_status_update(1)

		utils_obj.scroll_to_leader()
		return

	def delayed_monsters(self):
		return 0

	def monster_setup(self, npc, encounter_name, monster_code_name, monster_name, no_draw = 1, no_kos = 1, faction = None):
		super(CtrlCastleMain, self).monster_setup(npc, encounter_name, monster_code_name, monster_name, no_draw, no_kos, faction)
		npc.scripts[const_toee.sn_dying] = CASTLE_MAIN_DAEMON_SCRIPT
		return

	def get_dialogid_default(self):
		return CASTLE_MAIN_DAEMON_DIALOG

	def get_monster_faction_default(self, npc):
		return factions_zmod.FACTION_ENEMY

	def get_monster_prefix_default(self):
		return "CASTLE_MAIN"

	def critter_dying(self, attachee, triggerer):
		super(CtrlCastleMain, self).critter_dying(attachee, triggerer)
		assert isinstance(attachee, toee.PyObjHandle)
		return
