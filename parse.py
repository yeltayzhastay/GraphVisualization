import vk
import time

# https://oauth.vk.com/authorize?client_id=7651557&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,groups&response_type=token&v=5.130

class parse: # add token after that run get_groups_users
    def __init__(self, token):
        session = vk.Session(access_token=token)
        self.vk_api = vk.API(session)

    def __get_members(self, groupid): # additional method for parsing members
        first = self.vk_api.groups.getMembers(group_id=groupid, v=5.92)
        data = first["items"]
        count = first["count"] // 1000
        count = 10
        for i in range(1, count+1):  
            data = data + self.vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i*1000)["items"]
        return data
    
    def get_groups_users(self, groups_list): # Main method for parsing data
        groups_out = []
        for group_url in groups_list:
            try:
                list_of_group = self.__get_members(group_url)
                groups_out.append((group_url, {'count': len(list_of_group), 'users': list_of_group}))
            except:
                pass
        return groups_out