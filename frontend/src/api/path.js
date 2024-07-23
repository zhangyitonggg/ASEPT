const base = {
    baseUrl: 'http://localhost:8000',
    login: '/security/token',
    logon: '/create_user',
    news_getannouncements: '/news/get_announcements?max_announcements=20',
    showJoinedGroups: '/user_group/show_joined_groups',
    leaveGroup: '/user_group/leave_group',
    showCreatedGroups: '/user_group/show_create_groups',
    createGroup: '/user_group/create_group',
    modifyGroup: '/user_groupmodify_group',
    showUnGroups: '/user_group/show_unentered_groups',
}

export default base;