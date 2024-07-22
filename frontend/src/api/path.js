const base = {
    baseUrl: 'http://localhost:8000',
    login: '/security/token',
    logon: '/create_user',
    news_getannouncements: '/news/get_announcements?max_announcements=20',
    showJoinedGroups: '/user_group/show_joined_groups'
}

export default base;