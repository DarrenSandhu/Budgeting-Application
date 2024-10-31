
# I modified code we used for our small group project - is that okay? ~ Miriam 

from django.shortcuts import redirect

class ViewFilter:
    def prohibit_anonymous(view_function):
        def modified_view_function(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_function(request, *args, **kwargs)
            else:
                return redirect('log_in')
        return modified_view_function

