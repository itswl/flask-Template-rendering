"""
create by gaowenfeng on 
"""
from app.libs.enums import PendingStatus

__author__ = "gaowenfeng"

# 先处理单个，后处理一组

class DriftCollection:

    def __init__(self, drifts, current_user_id):
        self.data = []

        self.data = self._parse(drifts, current_user_id)

    def _parse(self, drifts, current_user_id):
        return [DriftViewModel(drift, current_user_id).data for drift in drifts]


class DriftViewModel:

    def __init__(self, drift, current_user_id):
        self.data = {}

        self.data = self._parse(drift, current_user_id)

    @staticmethod   # 判断到底是赠送者还是索要者
    def requester_or_gifter(drift, current_user_id):
        # 不建议将current_user耦合进DriftViewModel，破坏了封装性，难以扩展，所以当做参数从外部传入
        return 'requester' if current_user_id == drift.requester_id else 'gifter'

    def _parse(self, drift, current_user_id):
        you_are = DriftViewModel.requester_or_gifter(drift, current_user_id)
         # pending_status 设计到了4*2=8种状态，这个状态的判断应该在PendingStatus完成
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        r = {
            'drift_id': drift.id,
            'you_are': you_are,
            'book_title': drift.book_title,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': drift.create_datetime.strftime('%Y-%m-%d'),
            'operator': drift.requester_nickname if you_are != 'requester' \
                else drift.gifter_nickname,  # 显示请求者或赠送者的名字
            'message': drift.message,
            'address': drift.address,
            'status_str': pending_status,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending
        }

        return r
