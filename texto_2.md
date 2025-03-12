Posit Connect can integrate with your company’s Active Directory (AD) infrastructure using the LDAP authentication provider.

Using this integration, user authentication, group search, and user search requests will be directed to your LDAP service.

Posit Connect requires service credentials to execute user and group searches in Active Directory.

Note

If you are not able to obtain service credentials, you can still use Active Directory solely for authentication purposes with your own user credentials by configuring Posit Connect to use [Active Directory without Service Credentials](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-single-bind/).

## Active Directory Example With Service credentials [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#active-directory-example-with-service-credentials)

This sample configuration (partial) assumes the standard schema for Active Directory.

Note

The [Advanced LDAP / AD](https://docs.posit.co/connect/admin/appendix/advanced-ldap/) and [LDAP configuration](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP) appendixes contain more detailed information about each LDAP configuration option.

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg

[Authentication]
Provider = ldap

[LDAP "Sample AD Configuration With Service Credentials"]

; Connectivity

; For legacy SSL (ldaps) use these:
ServerAddress = ldaps.company.com:636
TLS = true
; Or for TLS (StartTLS extension) use these:
; ServerAddress = ldap.company.com:389
; StartTLS = true

TLSCACertificate= /etc/ssl/cert/ca.pem
; For TLS/SSL testing purposes only:
; ServerTLSInsecure = true

; Service credentials (recommended):
BindDN = "EXAMPLE\\admin"
BindPassword = "XXXXXXXX"
; Or anonymous bind (less secure):
; AnonymousBind = true

; Users
UserSearchBaseDN = "OU=Users,DC=example,DC=com"
UserObjectClass = "user"
UniqueIdAttribute = "objectGUID"
UsernameAttribute = "sAMAccountName"
UserEmailAttribute = "mail"
UserFirstNameAttribute = "givenName"
UserLastNameAttribute = "sn"

; Groups
GroupSearchBaseDN = "OU=Users,DC=example,DC=com"
GroupObjectClass = "group"
GroupUniqueIdAttribute = "objectGUID"
GroupNameAttribute = "sAMAccountName"
; Enable this for a better user experience, unless
; managing a large number of groups is a concern:
;GroupsAutoProvision = true

; When troubleshooting an LDAP problem, more verbose logging
; is produced by uncommenting the following line:
;Logging = true
```

## User provisioning [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#user-provisioning)

Active Directory users are created in Posit Connect upon the first successful login attempt.

Users can also be created ahead of their first login by adding them as users within the **People** tab of the Posit Connect dashboard or by using the Connect Server API.

[`LDAP.RegisterOnFirstLogin`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.RegisterOnFirstLogin) can be used to disable the registration through login behavior.

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[LDAP "corporate Active Directory"]
RegisterOnFirstLogin = false
```

Connect collects the user’s credentials and forward them to the Active Directory server which validates the authentication. If valid, the remote user’s information is returned to Connect.

Users within Posit Connect are assigned [Roles](https://docs.posit.co/connect/admin/user-management/#user-roles). Users are assigned the role specified by the [`Authorization.DefaultUserRole`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.DefaultUserRole) setting or one defined by the [User Role Mapping](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#user-role-mapping) if configured. Additionally, an administrator can reassign the role from within the dashboard or via the User Manager CLI.

### Usernames [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#usernames)

Usernames are controlled by your Active Directory server. However, Posit Connect imposes some additional restrictions on the usernames it supports:

- A username or DN containing a forward slash ( `/`) is not supported.
- The following values are prohibited: `connect`, `apps`, `users`, `groups`, `setpassword`, `user-completion`, `confirm`, `recent`, `reports`, `plots`, `unpublished`, `settings`, `metrics`, `tokens`, `help`, `login`, `welcome`, `register`, `resetpassword`, `content`

#### Duplicate usernames [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#duplicate-usernames)

Usernames in Active Directory do not need to be unique. A user is uniquely identified by the attribute defined in [`LDAP.UniqueIdAttribute`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.UniqueIdAttribute). (Users with the same username are differentiated via their personal passwords.)

Duplicate usernames are a reality of large Active Directory deployments with multiple servers, which implies multiple Active Directory server configurations in Posit Connect.

Warning

Active Directory global catalog configurations can also return duplicate usernames. However, that happens over a single connection which means a search for a username may return multiple hits. This configuration is not currently supported by Posit Connect.

Note

The RStudio IDE does not support duplicate usernames when publishing to the same Posit Connect host. However, it is unlikely that two users with the same usernames will be sharing the same IDE account or workstation.

Note

Duplicate users may have adverse affects on content that tracks the user credentials. Please refer to the [Credentials for Content](https://docs.posit.co/connect/admin/appendix/advanced-user-group/#content-credentials) in the [Advanced Users and Group Topics](https://docs.posit.co/connect/admin/appendix/advanced-user-group/) appendix for alternatives under this condition.

### User attributes [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#user-attributes)

The following user information is required:

- First name.
- Last name.
- Email address.
- Username.

Different Active Directory attributes may be used for each of these fields, but in general, all user attributes are provided by Active Directory, and they should all be present in the Posit Connect configuration.

Note

If your Active Directory server cannot provide some of these, be sure to not define the respective attributes in the Posit Connect configuration, so that the profile information can be entered manually by users. Otherwise, the profile values will not be editable in Posit Connect and will remain blank.

When changes are made to a user’s name, email address, or username in your Active Directory system, these changes will automatically propagate to Posit Connect:

- The next time that the user logs into Connect.
- When the user is returned in a search result while adding new users.
- As Connect synchronizes Active Directory group memberships.

#### Editing user attributes [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#editing-user-attributes)

A username is the primary means of authentication. Therefore, it is required in the configuration, and never editable.

By default, the setting [`Authorization.UserInfoEditableBy`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserInfoEditableBy) has a value of `AdminAndSelf`, permitting users and administrators to manage these editable user profile information not configured to be managed by Active Directory.

Configure [`Authorization.UserInfoEditableBy`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserInfoEditableBy) with `Admin` if profile editing should be restricted only to administrators.

Note

It is recommended that if you disable [`LDAP.RegisterOnFirstLogin`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.RegisterOnFirstLogin) with a value of `false`, that you also configure [`Authorization.UserInfoEditableBy`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserInfoEditableBy) to `Admin`. A value of `Admin` means that users created by the administrator, cannot be changed by non-administrators.

#### Editing user roles [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#editing-user-roles)

User roles are only editable in Posit Connect if [Automatic User Role Mapping](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#user-role-mapping) is not configured, and the Active Directory authentication provider is not configured to send roles in as part of the user profile.

### Automatic user role mapping [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#user-role-mapping)

Posit Connect offers ways to map their user information to valid roles when users login. This can be done with roles defined as part of the user profile or via [Active Directory group](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#ldap-groups) memberships.

#### Using group memberships [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#using-group-memberships)

Important

This option is not supported when using [Locally Managed Groups](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#local-groups).

Use the configuration option [`Authorization.UserRoleGroupMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleGroupMapping) to enable user role mapping via groups.

Note

When group mapping is enabled, configuration options to receive roles from the authentication provider as part of the user profile information is ignored and Connect will fail to start if [`Authorization.UserRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleMapping) is also enabled.

When enabled, the configuration options [`Authorization.ViewerRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.ViewerRoleMapping), [`Authorization.PublisherRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.PublisherRoleMapping), and [`Authorization.AdministratorRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.AdministratorRoleMapping) refer to groups.

In the following example, group names are used. Viewer mapping is purposely left out so that the remaining of the users are assigned the based on the option [`Authorization.DefaultUserRole`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.DefaultUserRole) which defaults to `viewer`.

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[Authorization]
UserRoleGroupMapping = true
PublisherRoleMapping = "cn=Developers,ou=Groups,dc=example,dc=com"
AdministratorRoleMapping = "cn=Dev-Leaders,ou=Groups,dc=example,dc=com"
AdministratorRoleMapping = "cn=IT-Administrators,ou=Groups,dc=example,dc=com"
```

#### Using user profile roles [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#using-user-profile-roles)

Use the configuration option [`LDAP.UserRoleAttribute`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.UserRoleAttribute) to enable user role mapping via a user profile attribute from your authentication provider.

The [`Authorization.UserRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleMapping) configuration option should also be used if the values you receive from your authentication provider do not match the default expected values of `viewer`, `publisher` and `administrator`.

Note

User roles can be used directly from your authentication provider without the need of mapping values as long as it only returns the values of `viewer`, `publisher` and `administrator` to define roles in Posit Connect.

**Example**

```sourceCode ini
# LDAP Record with no role mapping needed
uid: RUser
rsc-role: administrator

# Posit Connect Configuration to enable RUser
[LDAP "My LDAP Server Name"]
UserRoleAttribute = rsc-role

# LDAP Record with role mapping needed
uid: RUser2
rsc-role: connect-administrator

# Posit Connect Configuration to enable RUser2
[LDAP "My LDAP Server Name"]
UserRoleAttribute = rsc-role

[Authorization]
UserRoleMapping = true
AdministratorRoleMapping = connect-administrator
; PublisherRoleMapping = connect-publisher ; assuming the values continue as such
; ViewerRoleMapping = connect-viewer
```

When mapping is enabled, each role can be mapped to one or more values specific to your organization using the configuration options [`Authorization.ViewerRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.ViewerRoleMapping), [`Authorization.PublisherRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.PublisherRoleMapping), and [`Authorization.AdministratorRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.AdministratorRoleMapping).

In the following example the authentication provider returns department names:

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[Authorization]
UserRoleMapping = true
ViewerRoleMapping = "HR"
ViewerRoleMapping = "Marketing"
PublisherRoleMapping = "Engineering"
AdministratorRoleMapping = "IT"
```

#### Multiple user role mappings [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#multiple-user-role-mappings)

When there are multiple matches between the configured mapping and the user or group information sent by the authentication provider, the role with the most privileges is selected. This behavior makes it easy to promote users to a new role.

Note

If there are concerns about security, a more restrictive behavior can be used in these scenarios with the configuration option [`Authorization.UserRoleMappingRestrictive`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleMappingRestrictive). When enabled, it will cause the least privileged role to be selected.

## Active Directory groups [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#ldap-groups)

Posit Connect automatically associates users to the groups already present in Connect for access control purposes as indicated by the existing group memberships in Active Directory.

Warning

[Nested groups](https://docs.microsoft.com/en-us/windows/win32/ad/nesting-a-group-in-another-group) are not supported for Active Directory.

Connect needs to be configured to automatically recognize Active Directory groups. If the settings for groups are omitted from the configuration, only [Locally Managed Groups](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#local-groups) will be available.

Important

Active Directory groups **must** be managed directly through your Active Directory provider. Posit Connect does not support management of Active Directory groups.

A reference to a Active Directory group is stored in Connect when manually added via the **People** tab in the dashboard, via Connect Server API or automatically on log-in with the `LDAP.GroupsAutoProvision` setting enabled.

Changes made to group names and Distinguished Named automatically propagate to Connect:

- The next time that a member of the groups logs into Connect.
- When the group is returned in a search result while adding new groups.
- As Connect synchronizes Active Directory group memberships.

Active Directory groups are uniquely identified by the attribute defined in [`LDAP.GroupUniqueIdAttribute`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.GroupUniqueIdAttribute) (with the default of `"DN"`). For information on how to configure this setting for your specific Active Directory server, see [`GroupUniqueIdAttribute`](https://docs.posit.co/connect/admin/appendix/advanced-ldap/#group-unique-id-attribute).

### Manual group provisioning [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#manual-group-provisioning)

Admins can use the **People** tab within the Connect dashboard to add references to groups from the proxy. Group membership of Connect users is tracked for only these groups and not the entire list of groups that are returned from Active Directory.

Note

This is the default behavior, and a good option when the Connect users are associated with a large number of groups, but only some of them are useful for content access control purposes.

Warning

Care should be taken when removing groups via the **People** tab in the dashboard or via Connect Server API. Removing a group also removes all associations between the group being removed and existing content.

### Automatic group provisioning [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#automatic-group-provisioning)

In addition to delegating group membership management to Active Directory, Posit Connect can also delegate the management of groups themselves. By using [`LDAP.GroupsAutoProvision`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.GroupsAutoProvision)

Connect automatically adds references to groups based on the list of group memberships received from Active Directory during authentication.

With this option enabled groups are provisioned in Connect when the first member is added. These provisioned groups remain there indefinitely, even after the last member has been removed, so that any access to content is preserved for a future member of those groups.

Groups can be removed in the dashboard, using the Posit Connect Server API, or with the `usermanager` CLI.

### Active Directory group membership synchronization [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#group-membership-synchronization)

Posit Connect prefetches all group memberships during every authentication. After that, the group memberships for Active Directory users in Posit Connect are updated in a regular interval to ensure that content access granted via groups is synchronized with Active Directory.

By default, Connect updates each user individually every 4 hours, obtaining all their group memberships in the same way it is done during authentication. This interval can be modified via the configuration setting [`LDAP.MembershipUpdateInterval`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.MembershipUpdateInterval).

Important

In previous releases of Posit Connect, access controls validated group memberships directly with the Active Directory server at access time. This approach prevented Connect from having a complete picture of the group memberships for a given user, which in some situations resulted in reduced functionality when using LDAP authentication compared to other authentication providers.

Note

If you are running an earlier release of Posit Connect, an automatic synchronization for all users will take place immediately after an upgrade. Connect uses a best-effort approach to have all users updated within the configured [`LDAP.MembershipUpdateInterval`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.MembershipUpdateInterval) without disrupting the regular usage of the service. This process happens only once per installation and is not needed in future version upgrades.

Please see the [Performance Considerations](https://docs.posit.co/connect/admin/appendix/advanced-ldap/#performance) in the [Advanced LDAP / AD](https://docs.posit.co/connect/admin/appendix/advanced-ldap/) appendix for ways to optimize Active Directory search performance in Connect if you observe a noticeable impact on the service such as:

- Unusual delays during user log in.

- Modifications made to groups in Active Directory not being reflected in Connect _after_ the interval configured in [`LDAP.MembershipUpdateInterval`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.MembershipUpdateInterval) is passed.

- Issues with content with scheduled email delivery that include member of Active Directory groups.

- Excess of activity or usage on the Active Directory service.

- Warnings about the membership update process in the logs.


Note

The shorter the membership update interval, the greater the computational cost of running the synchronization. On the other hand, large or busy environments may need a longer update interval to be able to keep group memberships in sync consistently. The default interval value of 4 hours aims to offer a good balance between cost and user experience for most customers.

### Use Active Directory groups to limit access to Posit Connect [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#use-groups-to-limit-access-to-posit-connect)

By using Active Directory groups it is also possible to restrict which users are allowed in Posit Connect based on their group memberships. See the setting [`LDAP.PermittedLoginGroup`](https://docs.posit.co/connect/admin/appendix/advanced-ldap/#LDAP.PermittedLoginGroup) for more details.

### Scheduled email delivery & Active Directory group memberships [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#scheduled-email-delivery-group-memberships)

When using Active Directory groups associated to content, the recipients of content configured for scheduled email delivery will include all active and unlocked Connect users members of that group as well as all other Active Directory users members of the group with valid email addresses.

This functionality does not require or depend on the membership synchronization.

## Locally managed groups [Anchor](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#local-groups)

You can still use groups in Posit Connect if you decide to not configure support for Active Directory groups.

Important

Locally managed groups have no relation with Active Directory groups.

These groups are local to Connect, they can be created via the Dashboard or via the Connect Server API. Group memberships must also be managed using the same means.

If you do not want groups at all in Posit Connect, disable [`Authorization.UserGroups`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserGroups).