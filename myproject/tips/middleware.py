# myproject/tips/middleware.py

import random, time
from django.conf import settings

class AnonymousSessionMiddleware:
    """
    ユーザが未ログインの場合でも、匿名ユーザー名を 42秒間維持し、
    期限切れならランダムで再割り当てするミドルウェア。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # view を呼ぶ前にセッションをチェック
        self.ensure_anonymous_name(request)

        # view 処理
        response = self.get_response(request)

        # response を返す
        return response

    def ensure_anonymous_name(self, request):
        """
        セッション上にユーザー名と「割り当て時刻」が入っているか確認し、
        なければ新たにランダムで割り当てる。
        すでにある場合でも 42秒経過なら再度割り当て。
        """
        if not hasattr(settings, "ANONYMOUS_USERNAMES"):
            return  # 設定がなければ何もしない

        name_list = settings.ANONYMOUS_USERNAMES
        duration = getattr(settings, "ANONYMOUS_NAME_DURATION", 42)

        # セッションに既に匿名ユーザー名があるか確認
        anonymous_name = request.session.get("anonymous_name")
        assigned_time = request.session.get("anonymous_assigned_time")

        now = time.time()
        if not anonymous_name or not assigned_time:
            # 初回割り当て
            self.assign_new_name(request, name_list)
        else:
            # 期限切れかどうかチェック
            if (now - assigned_time) > duration:
                self.assign_new_name(request, name_list)

    def assign_new_name(self, request, name_list):
        """ランダムに名前を選んでセッションに保存"""
        chosen_name = random.choice(name_list)
        now = time.time()

        request.session["anonymous_name"] = chosen_name
        request.session["anonymous_assigned_time"] = now
