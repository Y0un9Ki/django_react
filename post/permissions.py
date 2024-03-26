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
    
'''
위에 클라스는 내가 직접 정의해준 클라스이다. permissions의 BasePermission을 상속받았다.
bool(request.user and request.user.is_superuser)코드는 'and' 연산자를 사용함으로써 2개가 다 True일때만 
겱과값이 True값이 나오게 코드를 만들었다. 
즉, request.user가 True이고 request.user가 superuser인게 True여야 리턴값으로 True값을 리턴하고 
True값이 리턴되었을 때 request요청에(Get, Post) 대해서 처리하라는 함수를 만든 것이다. 
간단히 요약하면 request.user가 superuser일 때 Get, Post를 처리하는 권한을 주는 클래스를 만든것이다.
'''