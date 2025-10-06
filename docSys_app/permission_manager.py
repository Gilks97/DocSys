
class PermissionManager:
    """Centralized permission checking"""
    
    @staticmethod
    def is_hod(user):
        return user.is_authenticated and user.user_type == 1
    
    @staticmethod
    def is_staff(user):
        return user.is_authenticated and user.user_type == 2
    
    @staticmethod
    def is_member(user):
        return user.is_authenticated and user.user_type == 3
    
    @staticmethod
    def has_staff_privileges(user):
        """Check if user has staff access (either staff user or member with privileges)"""
        if not user.is_authenticated:
            return False
        
        if user.user_type == 2:  # Regular staff
            return True
        elif user.user_type == 3 and hasattr(user, 'members'):  # Member with staff privileges
            return user.members.has_staff_privileges
        return False
    
    @staticmethod
    def can_access_staff_features(user):
        """Check if user can access staff features"""
        return PermissionManager.has_staff_privileges(user) or PermissionManager.is_hod(user)