=======
Signals
=======


`user_added`: dispatched from the `user_add` method on an organization. The sender is the organization, and the user is the provided arg.
`user_removed`: dispatched from the `user_remove` method on an organization. The sender is the organization, and the user is the provided arg.
`invitation_accepted`: dispatched from the ModeledInvitation backend. The sender is the ModelInvitation instance
`owner_changed`: dispatched from the `change_owner` method on an organization instance. The sender is the organization, and the `old` owner's organization user and the `new` owner's organization user are the providing args.
