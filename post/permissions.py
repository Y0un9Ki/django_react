from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 허용 하고 만약 요청자와 글의 주인이 동일한지 물어본다.
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return obj.user == request.user
    
    '''
    위에 코드는 permission에 해당하는 권한을 만들어 준것이며 SAFE_METHOD(GET, HEAD, OPTIONS)로 요청이 들어온 경우에는
    method를 허용해준다. 즉 get과 같이 그냥 보여주는 메서드는 허용을 하고, 그외 (PUT, PATCH, DELETE)와 같이 게시판을 
    수정하는 요청에는 게시글의 user와 request의 유저가 같을 때만 권한을 허용해준다.
    '''
    
class IsSuperUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)