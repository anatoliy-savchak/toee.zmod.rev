import toee
import utils_storage, utils_obj

def mayor_walk():
	mayor = utils_storage.ca("mayor_uptal").npc_get()
	print(mayor)
	mayor.anim_goal_push_goto(utils_obj.sec2loc(461, 474), 0)
	return

def mayor_walk2():
	mayor = utils_storage.ca("mayor_uptal").npc_get()
	print(mayor)
	#mayor.anim_goal_push_goto(utils_obj.sec2loc(461, 474), 0)
	#mayor.standpoint_set_ex(toee.STANDPOINT_DAY, utils_obj.sec2loc(461, 474))
	mayor.standpoint_set(toee.STANDPOINT_DAY, -1, utils_obj.sec2loc(459, 456), 0, 0, 0)
	return

def mayor_check():
	mayor = utils_storage.ca("mayor_uptal").npc_get()
	assert isinstance(mayor, toee.PyObjHandle)

	has_ONF_WAYPOINTS_DAY = mayor.npc_flags_get() & toee.ONF_WAYPOINTS_DAY
	print("ONF_WAYPOINTS_DAY: {}".format(has_ONF_WAYPOINTS_DAY))
	has_ONF_WAYPOINTS_NIGHT = mayor.npc_flags_get() & toee.ONF_WAYPOINTS_NIGHT
	print("ONF_WAYPOINTS_NIGHT: {}".format(has_ONF_WAYPOINTS_NIGHT))
	return
