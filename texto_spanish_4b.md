Posit Connect puede integrarse con la infraestructura de Active Directory (AD) de su empresa utilizando el proveedor de autenticación LDAP.

Mediante esta integración, las solicitudes de autenticación de usuarios, la búsqueda de grupos y las solicitudes de búsqueda de usuarios se dirigirán a su servicio LDAP.

Posit Connect requiere credenciales de servicio para ejecutar búsquedas de usuarios y grupos en Active Directory.

Nota

Si no puede obtener credenciales de servicio, aún puede utilizar Active Directory únicamente con fines de autenticación utilizando sus propias credenciales de usuario configurando Posit Connect para que use [Active Directory sin Credenciales de Servicio](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-single-bind/).

## Ejemplo de Active Directory Con Credenciales de Servicio [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#active-directory-example-with-service-credentials)

Esta configuración de ejemplo (parcial) asume el esquema estándar para Active Directory.

Nota

Los apéndices [LDAP Avanzado / AD](https://docs.posit.co/connect/admin/appendix/advanced-ldap/) y [Configuración LDAP](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP) contienen información más detallada sobre cada opción de configuración LDAP.

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg

[Authentication]
Provider = ldap

[LDAP "Ejemplo de AD Con Credenciales de Servicio"]

; Conectividad

; Para SSL heredado (ldaps) use estos:
ServerAddress = ldaps.company.com:636
TLS = true
; O para TLS (extensión StartTLS) use estos:
; ServerAddress = ldap.company.com:389
; StartTLS = true

TLSCACertificate= /etc/ssl/cert/ca.pem
; Para fines de prueba de TLS/SSL solamente:
; ServerTLSInsecure = true

; Credenciales de servicio (recomendado):
BindDN = "EXAMPLE\\admin"
BindPassword = "XXXXXXXX"
; O bind anónimo (menos seguro):
; AnonymousBind = true

; Usuarios
UserSearchBaseDN = "OU=Users,DC=example,DC=com"
UserObjectClass = "user"
UniqueIdAttribute = "objectGUID"
UsernameAttribute = "sAMAccountName"
```


```spanish
UserEmailAttribute = "mail"
UserFirstNameAttribute = "givenName"
UserLastNameAttribute = "sn"

; Grupos
GroupSearchBaseDN = "OU=Users,DC=example,DC=com"
GroupObjectClass = "group"
GroupUniqueIdAttribute = "objectGUID"
GroupNameAttribute = "sAMAccountName"
; Habilitar esto para una mejor experiencia de usuario, a menos que
; sea una preocupación administrar un gran número de grupos:
;GroupsAutoProvision = true

; Al solucionar problemas de LDAP, se produce un registro más detallado
; descomentando la siguiente línea:
;Logging = true
```

```spanish
## Provisionamiento de usuarios [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#user-provisioning)

Los usuarios de Active Directory se crean en Posit Connect en el primer intento de inicio de sesión exitoso.

Los usuarios también pueden ser creados antes de su primer inicio de sesión agregándolos como usuarios en la pestaña **People** del panel de control de Posit Connect o utilizando la API del Servidor Connect.

[`LDAP.RegisterOnFirstLogin`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.RegisterOnFirstLogin) se puede utilizar para deshabilitar el registro a través del comportamiento de inicio de sesión.

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[LDAP "directorio activo corporativo"]
RegisterOnFirstLogin = false
```

Posit Connect recopila las credenciales del usuario y las envía al servidor Active Directory, que valida la autenticación. Si es válida, la información del usuario remoto se devuelve a Posit Connect.

Los usuarios dentro de Posit Connect se asignan [Roles](https://docs.posit.co/connect/admin/user-management/#user-roles). Los usuarios se asignan al rol especificado por la configuración [`Authorization.DefaultUserRole`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.DefaultUserRole) o uno definido por la [Mapeo de Roles de Usuario](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#user-role-mapping) si está configurado. Además, un administrador puede reasignar el rol desde el panel de control o a través de la CLI User Manager.

### Nombres de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#usernames)

Los nombres de usuario están controlados por su servidor Active Directory. Sin embargo, Posit Connect impone algunas restricciones adicionales en los nombres de usuario que admite:

- Un nombre de usuario o DN que contenga una barra diagonal ( `/`) no está soportado.
- Los siguientes valores están prohibidos: `connect`, `apps`, `users`, `groups`, `setpassword`, `user-completion`, `confirm`, `recent`, `reports`, `plots`, `unpublished`, `settings`, `metrics`, `tokens`, `help`, `login`, `welcome`, `register`, `resetpassword`, `content`

#### Nombres de usuario duplicados [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#duplicate-usernames)

Los nombres de usuario en Active Directory no necesitan ser únicos. Un usuario se identifica de forma única mediante el atributo definido en [`LDAP.UniqueIdAttribute`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.UniqueIdAttribute). (Los usuarios con el mismo nombre de usuario se diferencian a través de sus contraseñas personales.)

Los nombres de usuario duplicados son una realidad de los despliegues de Active Directory de gran escala con múltiples servidores, lo que implica múltiples configuraciones de servidores Active Directory en Posit Connect.

Advertencia
```


Aquí está la traducción del texto proporcionado al español, sin resumir:

La configuración del catálogo global de Active Directory también puede devolver nombres de usuario duplicados. Sin embargo, esto ocurre en una sola conexión, lo que significa que una búsqueda de un nombre de usuario puede devolver múltiples resultados. Esta configuración no está actualmente soportada por Posit Connect.

Nota

El IDE RStudio no soporta nombres de usuario duplicados al publicar en el mismo host de Posit Connect. Sin embargo, es poco probable que dos usuarios con el mismo nombre de usuario compartan la misma cuenta de IDE o estación de trabajo.

Nota

Los usuarios duplicados pueden tener efectos adversos en el contenido que rastrea las credenciales del usuario. Consulte la sección [Credenciales para Contenido](https://docs.posit.co/connect/admin/appendix/advanced-user-group/#content-credentials) en la sección [Temas Avanzados de Usuarios y Grupos](https://docs.posit.co/connect/admin/appendix/advanced-user-group/) para alternativas bajo esta condición.

### Atributos de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#user-attributes)

La siguiente información del usuario es necesaria:

- Nombre de pila.
- Apellido.
- Dirección de correo electrónico.
- Nombre de usuario.

Pueden utilizarse diferentes atributos de Active Directory para cada uno de estos campos, pero en general, todos los atributos de usuario se proporcionan a través de Active Directory y deben estar presentes en la configuración de Posit Connect.

Nota

Si su servidor de Active Directory no puede proporcionar algunos de estos, asegúrese de no definir los atributos respectivos en la configuración de Posit Connect, para que la información del perfil pueda ser ingresada manualmente por los usuarios. De lo contrario, los valores del perfil no serán editables en Posit Connect y permanecerán en blanco.

Cuando se realizan cambios en el nombre, la dirección de correo electrónico o el nombre de usuario de un usuario en su sistema Active Directory, estos cambios se propagarán automáticamente a Posit Connect:

- La próxima vez que el usuario inicie sesión en Connect.
- Cuando el usuario se devuelve en un resultado de búsqueda al agregar nuevos usuarios.
- A medida que Connect sincroniza los grupos de Active Directory.

#### Edición de atributos de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#editing-user-attributes)

El nombre de usuario es el principal medio de autenticación. Por lo tanto, es requerido en la configuración y nunca editable.

Por defecto, la configuración [`Authorization.UserInfoEditableBy`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserInfoEditableBy) tiene un valor de `AdminAndSelf`, permitiendo que los usuarios y administradores gestionen la información de perfil de usuario no configurada para ser gestionada por Active Directory.

Configure [`Authorization.UserInfoEditableBy`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserInfoEditableBy) con `Admin` si la edición del perfil debe estar restringida solo a administradores.

Nota

Se recomienda que si desactiva [`LDAP.RegisterOnFirstLogin`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.RegisterOnFirstLogin) con un valor de `false`, también configure [`Authorization.UserInfoEditableBy`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserInfoEditableBy) a `Admin`. Un valor de `Admin` significa que los usuarios creados por el administrador no pueden ser cambiados por no administradores.

#### Edición de roles de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#editing-user-roles)

Los roles de usuario solo son editables en Posit Connect si [Mapeo Automático de Roles de Usuario](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#user-role-mapping) no está configurado, y el proveedor de autenticación de Active Directory no está configurado para enviar roles como parte del perfil de usuario.

### Mapeo automático de roles de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#user-role-mapping)


Posit Connect ofrece formas de mapear la información de sus usuarios a roles válidos cuando los usuarios se inician sesión. Esto se puede hacer con roles definidos como parte del perfil del usuario o a través de las membresías de [grupos de Active Directory](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#ldap-groups).

#### Usando las membresías de grupos [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#using-group-memberships)

Importante

Esta opción no está soportada cuando se utiliza [grupos administrados localmente](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#local-groups).

Utilice la opción de configuración [`Authorization.UserRoleGroupMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleGroupMapping) para habilitar el mapeo de roles de usuario a través de grupos.

Nota

Cuando se habilita el mapeo de grupos, las opciones de configuración para recibir roles del proveedor de autenticación como parte de la información del perfil del usuario se ignoran y Connect fallará al iniciarse si también está habilitado [`Authorization.UserRoleGroupMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleGroupMapping).

Cuando está habilitado, las opciones de configuración [`Authorization.ViewerRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.ViewerRoleMapping), [`Authorization.PublisherRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.PublisherRoleMapping), y [`Authorization.AdministratorRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.AdministratorRoleMapping) se refieren a grupos.

En el siguiente ejemplo, se utilizan nombres de grupo. El mapeo de visualizadores se deja deliberadamente sin incluir para que los usuarios restantes se asignen según la opción [`Authorization.DefaultUserRole`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.DefaultUserRole), que por defecto es `viewer`.

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[Authorization]
UserRoleGroupMapping = true
PublisherRoleMapping = "cn=Developers,ou=Groups,dc=example,dc=com"
AdministratorRoleMapping = "cn=Dev-Leaders,ou=Groups,dc=example,dc=com"
AdministratorRoleMapping = "cn=IT-Administrators,ou=Groups,dc=example,dc=com"
```

#### Usando roles del perfil de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#using-user-profile-roles)

Utilice la opción de configuración [`LDAP.UserRoleAttribute`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.UserRoleAttribute) para habilitar el mapeo de roles de usuario a través de un atributo de perfil de usuario de su proveedor de autenticación.

La opción de configuración [`Authorization.UserRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleMapping) también debe utilizarse si los valores que recibe de su proveedor de autenticación no coinciden con los valores esperados por defecto de `viewer`, `publisher` y `administrator`.

Nota

Los roles de usuario se pueden utilizar directamente de su proveedor de autenticación sin necesidad de mapear valores siempre que solo devuelva los valores de `viewer`, `publisher` y `administrator` para definir roles en Posit Connect.

**Ejemplo**

```sourceCode ini
# LDAP Record with no role mapping needed
uid: RUser
rsc-role: administrator

# Posit Connect Configuration to enable RUser
[LDAP "My LDAP Server Name"]
UserRoleAttribute = rsc-role

# LDAP Record with role mapping needed
uid: RUser2



rsc-role: administrador-connect

# Configuración de Posit Connect para habilitar RUser2
[LDAP "Mi Servidor LDAP Nombre"]
UserRoleAttribute = rsc-role

[Autorización]
UserRoleMapping = true
AdministratorRoleMapping = connect-administrator
; PublisherRoleMapping = connect-publisher ; asumiendo que los valores continúan de esta manera
; ViewerRoleMapping = connect-viewer

Cuando se habilita el mapeo, cada rol puede mapearse a uno o más valores específicos de su organización utilizando las opciones de configuración [`Autorización.ViewerRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.ViewerRoleMapping), [`Autorización.PublisherRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.PublisherRoleMapping) y [`Autorización.AdministratorRoleMapping`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.AdministratorRoleMapping).

En el siguiente ejemplo el proveedor de autenticación devuelve nombres de departamento:

```sourceCode ini
; /etc/rstudio-connect/rstudio-connect.gcfg
[Autorización]
UserRoleMapping = true
ViewerRoleMapping = "RRHH"
ViewerRoleMapping = "Marketing"
PublisherRoleMapping = "Ingeniería"
AdministratorRoleMapping = "IT"
```

#### Múltiples mapeos de roles de usuario [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#multiple-user-role-mappings)

Cuando hay múltiples coincidencias entre el mapeo configurado y la información del usuario o grupo enviada por el proveedor de autenticación, se selecciona el rol con los mayores privilegios. Este comportamiento facilita la promoción de usuarios a un nuevo rol.

Nota

Si existen preocupaciones sobre la seguridad, se puede utilizar un comportamiento más restrictivo en estos escenarios con la opción de configuración [`Autorización.UserRoleMappingRestrictive`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserRoleMappingRestrictive). Cuando está habilitada, seleccionará el rol con los menores privilegios.

## Grupos de Active Directory [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#ldap-groups)

Posit Connect asocia automáticamente a los usuarios a los grupos ya presentes en Connect para fines de control de acceso, según los existentes miembros de grupo en Active Directory.

Advertencia

[Grupos anidados](https://docs.microsoft.com/en-us/windows/win32/ad/nesting-a-group-in-another-group) no son compatibles con Active Directory.

Connect debe estar configurado para reconocer automáticamente los grupos de Active Directory. Si las configuraciones para los grupos se omiten de la configuración, solo estarán disponibles los [Grupos administrados localmente](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/#local-groups).

Importante

Los grupos de Active Directory **deben** ser administrados directamente a través de su proveedor de Active Directory. Posit Connect no admite la administración de grupos de Active Directory.

Se almacena una referencia a un grupo de Active Directory en Connect cuando se agrega manualmente a través de la pestaña **Personas** en el panel, a través de la API de Connect Server o automáticamente al iniciar sesión con la configuración `LDAP.GroupsAutoProvision` habilitada.


Cambios realizados en los nombres de grupo y Distinguished Named se propagan automáticamente a Connect:

- La próxima vez que un miembro de un grupo inicia sesión en Connect.
- Cuando el grupo se devuelve en un resultado de búsqueda al agregar nuevos grupos.
- Mientras Connect sincroniza los miembros de los grupos de Active Directory.

Los grupos de Active Directory se identifican de forma única por el atributo definido en [`LDAP.GroupUniqueIdAttribute`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.GroupUniqueIdAttribute) (con el valor predeterminado de `"DN"`). Para obtener información sobre cómo configurar esta configuración para su servidor de Active Directory específico, consulte [`GroupUniqueIdAttribute`](https://docs.posit.co/connect/admin/appendix/advanced-ldap/#group-unique-id-attribute).

### Provisionamiento de grupo manual [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#manual-group-provisioning)

Los administradores pueden usar la pestaña **Personas** dentro del panel de control de Connect para agregar referencias a grupos desde el proxy. La membresía en grupos de usuarios de Connect se rastrea solo para estos grupos y no para la lista completa de grupos que se devuelven de Active Directory.

Nota

Este es el comportamiento predeterminado y una buena opción cuando los usuarios de Connect están asociados con un gran número de grupos, pero solo algunos de ellos son útiles para el control de acceso al contenido.

Advertencia

Se debe tener cuidado al eliminar grupos a través de la pestaña **Personas** en el panel de control o a través de la API del Servidor Connect. Eliminar un grupo también elimina todas las asociaciones entre el grupo eliminado y el contenido existente.

### Provisionamiento de grupo automático [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#automatic-group-provisioning)

Además de delegar la gestión de la membresía en grupos a Active Directory, Posit Connect también puede delegar la gestión de los propios grupos. Al usar [`LDAP.GroupsAutoProvision`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.GroupsAutoProvision)

Connect agrega automáticamente referencias a grupos basadas en la lista de membresías en grupos recibida de Active Directory durante la autenticación.

Con esta opción habilitada, los grupos se provisionan en Connect cuando se agrega el primer miembro. Estos grupos provisionados permanecen allí indefinidamente, incluso después de que se haya eliminado el último miembro, para que se preserve el acceso al contenido para cualquier miembro futuro de esos grupos.

Los grupos se pueden eliminar en el panel de control, usando la API del Servidor Posit Connect o con la CLI `usermanager`.

### Sincronización de la membresía de grupo de Active Directory [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#group-membership-synchronization)

Posit Connect pre-recupera todas las membresías de grupo durante cada autenticación. Después de eso, las membresías de grupo para los usuarios de Active Directory en Posit Connect se actualizan en un intervalo regular para garantizar que el acceso al contenido otorgado a través de grupos se sincronice con Active Directory.

Por defecto, Connect actualiza cada usuario individualmente cada 4 horas, obteniendo todas sus membresías de grupo de la misma manera que se hace durante la autenticación. Este intervalo se puede modificar a través de la configuración del ajuste [`LDAP.MembershipUpdateInterval`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.MembershipUpdateInterval).

Importante

En versiones anteriores de Posit Connect, el control de acceso validaba las membresías de grupo directamente con el servidor de Active Directory en el momento de acceso. Este enfoque impedía que Connect tuviera una imagen completa de las membresías de grupo para un usuario determinado, lo que en algunas situaciones resultó en una funcionalidad reducida cuando se usaba la autenticación LDAP en comparación con otros proveedores de autenticación.

Nota

Si está ejecutando una versión anterior de Posit Connect, una sincronización automática para todos los usuarios tendrá lugar inmediatamente después de una actualización. Connect utiliza un enfoque de "mejor esfuerzo" para actualizar a todos los usuarios dentro del intervalo configurado [`LDAP.MembershipUpdateInterval`](https://docs.posit.co/connect/admin/appendix/configuration/#LDAP.MembershipUpdateInterval) sin interrumpir el uso regular del servicio. Este proceso ocurre solo una vez por instalación y no es necesario en futuras actualizaciones de versión.

Consulte la [Consideraciones de Rendimiento](https://docs.posit.co/connect/admin/appendix/advanced-ldap/#performance) en la sección [LDAP Avanzado](https://docs.posit.co/connect/admin/appendix/advanced-ldap/) para obtener más información.



Here’s the Spanish translation of the provided text, aiming for accuracy and including all content:

- Problemas con el envío de contenido por correo electrónico programado que incluyen miembros de grupos de Active Directory.

- Exceso de actividad o uso en el servicio de Active Directory.

- Advertencias sobre el proceso de actualización de membresía en los registros.

Nota:

El intervalo de actualización más corto implica un mayor coste computacional para la ejecución de la sincronización. Por otro lado, los entornos grandes o con mucha actividad pueden necesitar un intervalo de actualización más largo para poder mantener las membresías de grupo sincronizadas de forma consistente. El valor predeterminado del intervalo de 4 horas tiene como objetivo ofrecer un buen equilibrio entre coste y experiencia del usuario para la mayoría de los clientes.

### Utilice grupos de Active Directory para limitar el acceso a Posit Connect [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#use-groups-to-limit-access-to-posit-connect)

Al utilizar grupos de Active Directory, también es posible restringir a qué usuarios están permitidos en Posit Connect basándose en sus membresías de grupo. Consulte la configuración [`LDAP.PermittedLoginGroup`](https://docs.posit.co/connect/admin/appendix/advanced-ldap/#LDAP.PermittedLoginGroup) para obtener más detalles.

### Envío de correo electrónico programado y membresías de grupos de Active Directory [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#scheduled-email-delivery-group-memberships)

Cuando se utilizan grupos de Active Directory asociados al contenido, los destinatarios del contenido configurado para el envío de correo electrónico programado incluirán a todos los usuarios de Connect activos y desbloqueados miembros de ese grupo, así como a todos los demás usuarios de Active Directory miembros del grupo con direcciones de correo electrónico válidas.

Esta funcionalidad no requiere ni depende de la sincronización de la membresía.

## Grupos administrados localmente [Ancla](https://docs.posit.co/connect/admin/authentication/ldap-based/active-directory-double-bind/\#local-groups)

Todavía puede utilizar grupos en Posit Connect si decide no configurar el soporte para grupos de Active Directory.

Importante

Los grupos administrados localmente no tienen relación con los grupos de Active Directory.

Estos grupos son locales a Connect y pueden ser creados a través del Panel de Control o a través de la API del Servidor Connect. Las membresías de grupo también deben gestionarse utilizando los mismos medios.

Si no desea utilizar grupos en absoluto en Posit Connect, desactive [`Authorization.UserGroups`](https://docs.posit.co/connect/admin/appendix/configuration/#Authorization.UserGroups).


