services.service("xxMobile", ["$timeout", "xxHttp", "xxContext", function (e, t, r) {
    return {
        verify: function (a) {
            return {
                disablePwdInput: 1, disableSendBtn: 0, sendButtonText: "获取验证码", sendAuthCode: function () {
                    var n = this;
                    if (this.mobile == null || !/^1\d{10}$/.test(this.mobile)) {
                        alert("请输入正确的手机号");
                        return
                    }
                    var o = function () {
                        if (n.count > 0) {
                            n.count--;
                            n.sendButtonText = n.count + "秒后重发";
                            e(o, 1e3)
                        } else {
                            n.disableSendBtn = 0;
                            n.sendButtonText = "重发验证码"
                        }
                    };
                    t.get("/server/publics/user/auth_code", false, function (t) {
                        n.disablePwdInput = 0;
                        n.count = 60;
                        o();
                        if (!r.isIOS()) {
                            e(function () {
                                document.getElementById("authCode").focus()
                            }, 200)
                        }
                    }, {params: {mobile: n.mobile, mustNew: a}}, function (e, t) {
                        n.disableSendBtn = 0;
                        alert(t)
                    }, function () {
                        n.sendButtonText = "重发验证码";
                        n.disableSendBtn = 0;
                        alert("验证码发送失败，请重试")
                    });
                    this.disableSendBtn = 1
                }
            }
        }
    }
}]);
var directives = angular.module("xxDirective", ["xxService"]);
directives.directive("xxB5f", ["$location", "xxHttp", function (e, t) {
    return {
        restrict: "E",
        replace: true,
        transclude: true,
        scope: {
            varName: "=xxVarName",
            factor: "=xxFactor",
            score: "=xxScore",
            options: "=xxOptions",
            accuracy: "=xxAccuracy",
            exams: "=xxExams",
            suggestion: "=xxSuggestion"
        },
        link: function (r, a, n, o) {
            r.getHistory = function () {
                t.get("/server/publics/auth/user/php/history", false, function (e) {
                    r.his = e
                }, {params: {factor: r.varName}})
            };
            r.unlock = function () {
                t.get("/server/publics/exam_type", true, function (t) {
                    if (t.content.length > 0) {
                        if (confirm("通过《" + t.content[0].fullName + "》开始解锁？\n(下周期生效)")) {
                            e.path("/exam/" + t.content[0].id + "/null/null")
                        }
                    } else {
                        alert("抱歉，香蕉君暂时想不出办法帮你解锁")
                    }
                }, {params: {type_name: r.exams, page: 0, size: 1}})
            }
        },
        templateUrl: "views/my/b5f_factor.html"
    }
}]);
var app = angular.module("xqxj", ["ngRoute", "ngTouch", "mobile-angular-ui", "chart.js", "xxService", "xxDirective", "xxFilter"]);
var appRouteConfig = ["$routeProvider", "$locationProvider", function (e, t) {
    e.when("/", {
        controller: homeCtlr,
        templateUrl: "views/home.html",
        auth: false
    }).when("/login", {
        controller: loginCtlr,
        templateUrl: "views/login.html",
        auth: false
    }).when("/user_center", {
        controller: centerCtlr,
        templateUrl: "views/my/user_center.html"
    }).when("/cnslr", {
        controller: cnslrGalaryCtlr,
        templateUrl: "views/counselor/galary.html",
        auth: false
    }).when("/cnslr/:id", {
        controller: cnslrDetailCtlr,
        templateUrl: "views/counselor/detail.html",
        auth: false
    }).when("/cnslr/:id/appoint", {
        controller: cnslrAppointCtlr,
        templateUrl: "views/counselor/appoint.html"
    }).when("/cnslr/note/:id", {
        controller: noteCtlr,
        templateUrl: "views/counselor/note.html",
        auth: false
    }).when("/balance/center", {
        controller: balanceCenterCtlr,
        templateUrl: "views/balance/center.html"
    }).when("/balance/weixinpay", {
        controller: balanceWeixinPayCtlr,
        templateUrl: "views/balance/weixinpay.html"
    }).when("/balance/alipay", {
        controller: balanceAliPayCtlr,
        templateUrl: "views/balance/alipay.html"
    }).when("/balance/ticket", {
        controller: balanceTicPayCtlr,
        templateUrl: "views/balance/ticket.html"
    }).when("/balance/flow", {
        controller: balanceFlowCtlr,
        templateUrl: "views/balance/flow.html"
    }).when("/dial/records", {
        controller: dialRecordsCtlr,
        templateUrl: "views/dial/records.html"
    }).when("/dial/:id", {
        controller: dialDetailCtlr,
        templateUrl: "views/dial/detail.html"
    }).when("/chat/main/:counselor_id", {
        controller: chatMainCtlr,
        templateUrl: "views/chat/main.html"
    }).when("/chat/record", {
        controller: chatRecordCtlr,
        templateUrl: "views/chat/record.html"
    }).when("/fav_cnslr_list", {
        controller: attenListCtlr,
        templateUrl: "views/my/fav_cnslr_list.html"
    }).when("/apply", {
        controller: applyCounselorCtlr,
        templateUrl: "views/counselor/apply_cnslr.html"
    }).when("/my/nav", {templateUrl: "views/my/nav/main.html"}).when("/my/nav/consult", {templateUrl: "views/my/nav/consult.html"}).when("/my/nav/exam", {templateUrl: "views/my/nav/exam.html"}).when("/exam/list", {
        controller: examListCtlr,
        templateUrl: "views/exam/exam_list.html",
        auth: false
    }).when("/pay/exam", {
        controller: examOrderCtlr,
        templateUrl: "views/exam/exam_order.html",
        auth: false
    }).when("/exam/list/finish", {
        controller: finishExamListCtlr,
        templateUrl: "views/exam/finish_exam_list.html"
    }).when("/exam/report/:exam_id", {
        controller: examReportCtlr,
        templateUrl: "views/exam/exam_report.html",
        auth: false
    }).when("/exam/:exam_type_id/:member_id/:group_id", {
        controller: examCtlr,
        templateUrl: "views/exam/exam.html",
        auth: false
    }).when("/settings", {
        controller: settingsCtlr,
        templateUrl: "views/my/settings.html"
    }).when("/my/php", {
        controller: myPhpCtlr,
        templateUrl: "views/my/php.html",
        auth: false
    }).when("/sales", {
        controller: salesCtlr,
        templateUrl: "views/sales/main.html"
    }).when("/sales/links", {
        controller: salesLinksCtlr,
        templateUrl: "views/sales/links.html"
    }).when("/sales/brokerage", {
        controller: salesBrokerageCtlr,
        templateUrl: "views/sales/brokerage.html"
    }).when("/sales/order_list", {
        controller: salesOrderListCtlr,
        templateUrl: "views/sales/order_list.html"
    }).when("/sales/referral", {
        controller: salesReferralCtlr,
        templateUrl: "views/sales/referral.html"
    }).when("/pack/career", {
        controller: packCtrl,
        templateUrl: "views/pack/career.html",
        auth: false
    }).when("/pack/health", {
        controller: packCtrl,
        templateUrl: "views/pack/health.html",
        auth: false
    }).when("/pack/emotion", {
        controller: packCtrl,
        templateUrl: "views/pack/emotion.html",
        auth: false
    }).otherwise({redirectTo: "/"});
    t.html5Mode(true)
}];
app.config(appRouteConfig);
app.run(userInitConfig);
app.run(["$rootScope", "$location", "$timeout", "xxHttp", function (e, t, r, a) {
    t.search().no_cnslr && sessionStorage.setItem("no_cnslr", true);
    var n = t.search().ult;
    if (n) {
        e.setLogin({id: n});
        e.loadCurrentUser()
    }
    e.showCnslr = function () {
        return !sessionStorage.getItem("no_cnslr")
    };
    t.search().no_menu && sessionStorage.setItem("no_menu", true);
    e.showMenu = function () {
        return !sessionStorage.getItem("no_menu")
    };
    sessionStorage.setItem("landingUrl", t.search().direct && document.referrer ? document.referrer : t.absUrl());
    e.href = function (e) {
        location.href = e
    };
    e.loadSeller = function (t) {
        if (!e.seller || t) {
            a.get("/server/publics/auth/user/sales/seller", true, function (t) {
                if (t) {
                    var r = function (e, t) {
                        var r = 0, a = 0, n = 0, o = {};
                        for (var i in t) {
                            var l = parseFloat(i);
                            a = t[i];
                            if (e > l) {
                                o[a] = l - r;
                                n += a * (l - r);
                                r = l
                            } else {
                                var s = e - r;
                                o[a] = s;
                                n += a * s;
                                r = e;
                                break
                            }
                        }
                        if (e > r) {
                            var s = e - r;
                            n += a * s;
                            o[a] = o[a] + s
                        }
                        return {value: n, equation: o}
                    };
                    t.brokerage = [r(t.unsettledSale, t.ratios), r(t.referralUnsettledSale, t.referralRatios)]
                }
                e.seller = t
            })
        }
    };
    e.loginIfNot = function (r) {
        var a = !e.isUserLogin();
        if (a) {
            localStorage.setItem("login_back_path", r != null ? r : t.path());
            t.path("/login")
        }
        return a
    };
    e.$on("$routeChangeStart", function (a, n, o) {
        e.isUserLogin() && e.user == null && e.loadCurrentUser();
        n.auth = n.auth == null ? true : n.auth;
        if (n.auth && !e.isUserLogin()) {
            if (e.isWeiXin || e.isWeiBo || e.isQQ) {
                var i = function () {
                    if (e.autoLogin) {
                        r(i, 200)
                    } else {
                        t.search("code", null)
                    }
                };
                r(i, 200);
                a.preventDefault()
            } else {
                _hmt.push(["_trackPageview", "/login"]);
                e.loginIfNot()
            }
        } else {
            if (o && o.passThrough) {
                console.log("No track")
            } else {
                _hmt.push(["_trackPageview", t.path()])
            }
        }
    });
    e.initTitleDesc = function (t, r) {
        e.idx_title = t == null ? "心情香蕉" : t;
        e.idx_desc = r
    }
}]);
app.controller("MainCtrl", ["$rootScope", "$scope", "$window", "xxHttp", "xxMobile", "SharedState", function (e, t, r, a, n, o) {
    t.verify = n.verify(true);
    e.$on("$locationChangeStart", function (e) {
        if (o.isActive("messageModal")) {
            o.turnOff("messageModal");
            e.preventDefault()
        }
    });
    e.showMsgModal = function (t) {
        e.msg = t;
        t.n = function () {
            o.turnOff("messageModal");
            this.onNegative()
        };
        t.p = function () {
            o.turnOff("messageModal");
            this.onPositive()
        };
        o.turnOn("messageModal")
    };
    e.bindMobile = function () {
        a.post("/server/publics/auth/user/mobile", true, function (t) {
            e.user = t;
            alert("手机号绑定成功!");
            o.turnOff("bindMobileModal")
        }, t.verify.mobile, {params: {authCode: t.verify.authCode}})
    }
}]);
var homeCtlr = ["$rootScope", "$scope", "$location", "$timeout", "xxHttp", function (e, t, r, a, n) {
    t.cert = {company: "相交科技（武汉）有限公司", icp: "鄂ICP备15008675号-2", showAbout: true};
    t.certs = {"xqxj.zjxunsiwl.com": {company: "郑州讯思信息科技有限公司绍兴柯桥分公司", icp: "豫ICP备20018762号-2"}};
    t.initHomepage = function () {
        t.local_guide_path = localStorage.getItem("guide_path");
        if (t.local_guide_path != t.guide_path) {
            localStorage.setItem("guide_path", t.guide_path);
            t.tipGuide = true
        } else {
            t.guideClicked = localStorage.getItem("guide_clicked");
            t.tipGuide = t.guideClicked != 1
        }
        var e = t.certs[window.location.hostname];
        t.cert = e ? e : t.cert
    }();
    t.goto_guide = function () {
        localStorage.setItem("guide_clicked", 1);
        window.location = t.guide_path
    };
    t.gotoPack = function (t, a) {
        if (localStorage.getItem(a) || e.isPC) {
            r.path(t)
        } else {
            localStorage.setItem(a, true);
            window.location = a
        }
    }
}];
var loginCtlr = ["$rootScope", "$scope", "$location", "$window", "$timeout", "xxHttp", "xxMobile", function (e, t, r, a, n, o, i) {
    t.verify = i.verify(false);
    if (e.isPC) {
        var l = r.search().code;
        if (l != null) {
            e.autoLogin = true;
            o.get("/server/qq/login", true, function (t) {
                localStorage.setItem("user_token", JSON.stringify(t));
                e.setLogin(t);
                e.autoLogin = null
            }, {params: {redirect_uri: localStorage.getItem("user_qq_ru"), code: l}})
        }
    }
    t.qqLogin = function () {
        localStorage.setItem("user_qq_ru", r.absUrl());
        o.get("/server/qq/oauth", true, function (e) {
            a.location.href = e
        }, {params: {redirect_uri: encodeURIComponent(r.absUrl()), state: "Config"}})
    };
    var s = function () {
        var e = localStorage.getItem("login_back_path");
        localStorage.removeItem("login_back_path");
        if (e && e.substring(0, 4) == "http") {
            window.location.href = e
        } else {
            r.path(e == null ? "/" : e).replace()
        }
    };
    var c = function () {
        if (e.autoLogin) {
            n(c, 200)
        } else {
            e.isUserLogin() && s()
        }
    };
    c();
    t.goWX = function () {
        return sessionStorage.getItem("goWX") != null
    };
    t.submit = function () {
        if (t.verify.authCode == null || !/^\d{6}$/.test(t.verify.authCode)) {
            alert("验证码格式错误");
            return
        }
        var r = {mobile: t.verify.mobile, authCode: t.verify.authCode};
        o.get("/server/publics/user/login", function (e) {
            t.submiting = e
        }, function (t) {
            e.setLogin(t.user_token);
            localStorage.setItem("user_token", JSON.stringify(t.user_token));
            if (t.new_user && t.user_token.user.balance != 0) {
                alert("欢迎加入心情香蕉，" + t.user_token.user.balance + "元礼券已放入您的账户！")
            }
            s()
        }, {params: r})
    }
}];
var centerCtlr = ["$rootScope", "$scope", "xxHttp", "SharedState", function ($rootScope, $scope, xxHttp, SharedState) {
    $rootScope.loadCurrentUser();
    $scope.init_modify_info = function (e) {
        $scope.modify_user = {info: e}
    };
    $scope.modifyNickName = function () {
        if ($scope.modify_user.info == "") {
            return
        }
        xxHttp.put("/server/publics/auth/user", null, function () {
            SharedState.turnOff("modal_modify_nickName");
            $rootScope.loadCurrentUser()
        }, {nickName: $scope.modify_user.info})
    };
    $scope.modifyGender = function () {
        if ($scope.modify_user.info == "") {
            return
        }
        xxHttp.put("/server/publics/auth/user", null, function () {
            SharedState.turnOff("modal_modify_gender");
            $rootScope.loadCurrentUser()
        }, {gender: $scope.modify_user.info})
    };
    $scope.modifyBirthday = function () {
        var input_birthday = eval(document.getElementById("birthday")).value;
        if (input_birthday == undefined) {
            alert("亲，有这样的时间喵？");
            return
        }
        xxHttp.put("/server/publics/auth/user", null, function () {
            SharedState.turnOff("modal_modify_birthday");
            $rootScope.loadCurrentUser()
        }, {birthday: input_birthday})
    };
    $scope.modifyCareer = function () {
        xxHttp.put("/server/publics/auth/user", null, function () {
            SharedState.turnOff("modal_modify_career");
            $rootScope.loadCurrentUser()
        }, {career: $scope.modify_user.info})
    }
}];
var cnslrGalaryCtlr = ["$rootScope", "$scope", "$timeout", "xxHttp", "xxPage", "xxContext", "SharedState", function (e, t, r, a, n, o, i) {
    var l = angular.element(document.getElementById("cnslrContent"));
    var s = function (e, r, n, o) {
        a.get("/server/publics/counselors", o, n, {
            params: {
                skills: t.param_skills,
                genders: t.param_genders,
                generations: t.param_generations,
                sort: t.param_sort,
                page: e,
                size: r,
                keyword: t.param_keyword
            }
        })
    };
    t.reload = function () {
        t.param_keyword = null;
        t.param_skills = o.checkboxValue(t.input_skills);
        t.param_genders = o.checkboxValue(t.input_genders);
        t.param_generations = o.checkboxValue(t.input_generations);
        t.param_sort = t.input_sort + "," + t.input_direction;
        e.cnslrPage = n(s, 10)
    };
    t.setGender = function (e) {
        t.input_genders[e] = !t.input_genders[e]
    };
    t.setGeneration = function (e) {
        t.input_generations[e] = !t.input_generations[e]
    };
    t.setSkill = function (e) {
        t.input_skills[e.id] = !t.input_skills[e.id]
    };
    t.applySkill = function () {
        t.reload();
        i.turnOff("skillModal")
    };
    t.applyFilter = function () {
        t.reload();
        i.turnOff("filterModal")
    };
    t.applyOrder = function (e) {
        t.input_sort = e;
        t.input_direction = t.input_direction == "ASC" ? "DESC" : "ASC";
        t.reload();
        i.turnOff("orderModal")
    };
    t.unsearch = function () {
        t.searching = false;
        t.param_keyword != null && t.reload()
    };
    t.search = function () {
        t.param_keyword = t.input_keyword;
        t.param_skills = null;
        t.param_genders = null;
        t.param_generations = null;
        e.cnslrPage = n(s, 10)
    };
    a.get("/server/publics/counselor_skill", true, function (a) {
        t.input_skills = {};
        for (var n in a) {
            t.input_skills[a[n].id] = false
        }
        t.skills = a;
        if (e.cnslrPage == null || localStorage.getItem("cnslrAnchor") == null) {
            r(t.reload, 50)
        } else {
            r(function () {
                var e = l.controller("scrollableContent");
                e.scrollTo(document.getElementById(localStorage.getItem("cnslrAnchor")))
            }, 100)
        }
    })
}];
var cnslrDetailCtlr = ["$rootScope", "$scope", "$location", "$window", "$sce", "$routeParams", "$timeout", "xxHttp", "xxPage", "SharedState", function (e, t, r, a, n, o, i, l, s, c) {
    if (o.pro == "LR") {
        a.location.href = "http://gzh.zuta.biz/go.php?id=84"
    }
    e.configJsApi(["stopRecord"]);
    t.fetchCounselor = function () {
        l.get("/server/publics/counselor/" + o.id, true, function (r) {
            t.counselor = r;
            e.initTitleDesc(t.counselor.user.nickName + "的名片");
            t.currentProjectUrl = n.trustAsResourceUrl(t.counselor.voiceUrl);
            t.totalCalledSeconds = Math.ceil(t.counselor.totalCalledSeconds / 3600);
            var a = new Date;
            t.nowtime = a.getHours();
            t.stars = r.avgEvaluatedStars;
            e.wxShare(t.counselor.user.nickName, e.rootUrl + "/cnslr/" + t.counselor.id, t.counselor.photo + "?x-oss-process=style/11s", "心情香蕉\n认证咨询师 V")
        })
    };
    t.fetchCounselor();
    if (e.isUserLogin()) {
        l.get("/server/publics/auth/user/concern/" + o.id, false, function (e) {
            t.attenstatus = e.concernState ? e.concernState : false
        })
    }
    t.goAtten = function () {
        if (e.isUserLogin()) {
            l.put("/server/publics/auth/user/concern/" + o.id, false, function (e) {
                t.attenstatus = e.concernState
            })
        } else {
            e.loginIfNot()
        }
    };
    var u = function (e, t, r, a) {
        l.get("/server/publics/counselor/" + o.id + "/note", a, r, {params: {page: e, size: t}})
    };
    t.notePage = s(u, 10);
    t.playVoice = function () {
        var e = document.getElementById("audio");
        t.voiceStatus = !t.voiceStatus;
        if (t.voiceStatus) {
            e.pause();
            e.currentTime = 0
        } else {
            e.play()
        }
        e.addEventListener("ended", function () {
            i(function () {
                t.voiceStatus = true
            }, 1e3)
        }, false)
    }
}];
var cnslrAppointCtlr = ["$rootScope", "$scope", "$location", "$routeParams", "xxHttp", function (e, t, r, a, n) {
    n.get("/server/publics/counselor/" + a.id, true, function (o) {
        t.cnslr = o;
        n.get("/server/publics/auth/user/cnslr/" + a.id + "/schedule", true, function (e) {
            t.schedule = e
        });
        if (e.user.balance < o.dialUnitPrice) {
            e.showMsgModal({
                title: "余额不足",
                content: "本次咨询费用为<strong>" + o.dialUnitPrice + "</strong>元。<br/>为避免无效预约，请保证您的账户中有足够余额。",
                positive: "去充值",
                negative: "先看看",
                onPositive: function () {
                    r.path("/balance/center")
                },
                onNegative: function () {
                }
            })
        }
    });
    t.step = 1;
    t.switchDay = function (e) {
        if (e == t.dIdx) {
            t.dIdx = null
        } else {
            t.dIdx = e
        }
    };
    t.switchHour = function (e) {
        var r = t.schedule[t.dIdx];
        r.c = r.c == null ? 0 : r.c;
        t.c = t.c == null ? 0 : t.c;
        if (r.hours[e] == 2) {
            r.hours[e] = 1;
            r.c--;
            t.c--
        } else if (r.hours[e] == 1) {
            r.hours[e] = 2;
            r.c++;
            t.c++
        }
    };
    t.request = function () {
        var e = [];
        for (var o in t.schedule) {
            for (var i in t.schedule[o].hours) {
                if (t.schedule[o].hours[i] == 2) {
                    var l = t.schedule[o].day.split(/[- : \/]/);
                    e.push(new Date(l[0], l[1] - 1, l[2], i, 0, 0).getTime())
                }
            }
        }
        if (e.length == 0) {
            alert("请至少选择一个时间段预约。")
        } else {
            n.post("/server/publics/auth/user/dial_consult_record", true, function (e) {
                alert("预约成功!");
                r.path("/dial/" + e).replace()
            }, {counselor: {id: a.id}, userMobile: t.mobile, requestTimes: e})
        }
    }
}];
var balanceCenterCtlr = ["$rootScope", "$scope", "$location", "xxHttp", function (e, t, r, a) {
    t.loadBalance = function () {
        a.get("/server/publics/auth/user", true, function (r) {
            t.balance = r.balance;
            e.user.balance = r.balance
        }, {params: {fields: "balance_only"}})
    }();
    t.checkFlow = function () {
        r.path("/balance/flow")
    }
}];
var balanceWeixinPayCtlr = ["$rootScope", "$scope", "$location", "$document", "$window", "xxHttp", function (e, t, r, a, n, o) {
    t.startWeiXinPay = function () {
        WeixinJSBridge.invoke("getBrandWCPayRequest", weixinPayParams, function (e) {
            if (e.err_msg == "get_brand_wcpay_request:ok") {
                alert("充值成功!");
                r.path("/balance/center")
            } else {
                alert("充值失败!请重新支付[" + e.err_msg + "]")
            }
            localStorage.removeItem("charge_amount");
            r.search("showwxpaytitle", null);
            t.$apply()
        });
        t.$apply()
    };
    t.init = function () {
        if (!e.requestWeiXinPay) {
            if (r.search().showwxpaytitle == 1) {
                t.chargeAmount = localStorage.getItem("charge_amount");
                var n = JSON.parse(localStorage.getItem("user_token")).wxOpenUser.openId;
                if (t.chargeAmount != null && n != null) {
                    o.post("/server/publics/auth/user/charge/weixin/" + n, true, function (e) {
                        weixinPayParams = e;
                        if (typeof WeixinJSBridge == "undefined") {
                            a.bind("WeixinJSBridgeReady", t.startWeiXinPay)
                        } else {
                            t.startWeiXinPay()
                        }
                    }, t.chargeAmount)
                }
            }
        }
    }();
    t.requestWeiXinPay = function () {
        r.search("showwxpaytitle", 1);
        localStorage.setItem("charge_amount", t.chargeAmount);
        e.requestWeiXinPay = true;
        n.location.href = r.absUrl()
    }
}];
var balanceAliPayCtlr = ["$scope", "$location", "$window", "xxHttp", function (e, t, r, a) {
    e.requestAliPay = function () {
        a.get("/server/publics/auth/user/charge/alipay/wap", true, function (e) {
            r.location.href = e
        }, {params: {amount: e.chargeAmount}})
    };
    e.init = function () {
        var e = t.search();
        if (e.result != null) {
            a.post("/server/publics/auth/user/charge/alipay/wap", true, function (e) {
                alert("充值成功!");
                t.path("/balance/center")
            }, {
                result: e.result,
                sign: e.sign,
                out_trade_no: e.out_trade_no,
                trade_no: e.trade_no,
                request_token: e.request_token
            })
        }
    }()
}];
var balanceTicPayCtlr = ["$scope", "$location", "xxHttp", function (e, t, r) {
    e.convert = function () {
        var a = e.ticket.split("_");
        r.put("/server/publics/auth/user/charge/coupon", null, function (e) {
            alert("兑换成功!请您前往香蕉余额查看余额!");
            t.path("/balance/center")
        }, {id: a[0], verifyCode: a[1]})
    }
}];
var balanceFlowCtlr = ["$scope", "xxHttp", "xxPage", function (e, t, r) {
    var a = function (e, r, a, n) {
        t.get("/server/publics/auth/user/balance_flow", n, a, {params: {page: e, size: r}})
    };
    e.bfPage = r(a, 10)
}];
var dialRecordsCtlr = ["$scope", "xxHttp", "xxPage", function (e, t, r) {
    var a = function (e, r, a, n) {
        t.get("/server/publics/auth/user/consult/call", n, a, {params: {page: e, size: r}})
    };
    e.dcrPage = r(a, 10)
}];
var dialDetailCtlr = ["$scope", "$location", "$routeParams", "xxHttp", function (e, t, r, a) {
    e.load = function () {
        a.get("/server/publics/auth/user/consult/call/" + r.id, true, function (t) {
            e.dialRecord = t
        }, {params: {fields: "detail"}})
    };
    e.load();
    e.submit = function () {
        if (e.stars < 3) {
            if (e.msg == null) {
                alert("请说说不满意的原因吧");
                return
            }
        }
        a.post("/server/publics/auth/user/consult/call/" + r.id + "/stars", true, function (t) {
            e.dialRecord.evaluatedStars = e.stars;
            alert("评分提交成功")
        }, {evaluatedStars: e.stars, evaluatedContent: e.msg})
    };
    e.complaint = function () {
        t.path("/complaint/" + r.id).replace()
    };
    e.cancel = function () {
        a.delete("/server/publics/auth/user/dial_consult_record/" + r.id, true, function (t) {
            alert("预约已成功取消");
            e.load()
        })
    }
}];
var chatRecordCtlr = ["$rootScope", "$scope", "$routeParams", "xxHttp", "xxPage", function (e, t, r, a, n) {
    e.configJsApi(["stopRecord"]);
    var o = function (e, t, r, n) {
        a.get("/server/publics/auth/user/conversation", n, r, {params: {page: e, size: t}})
    };
    t.chatPage = n(o, 20)
}];
var chatMainCtlr = ["$rootScope", "$scope", "$location", "$timeout", "$routeParams", "xxHttp", "xxPage", "$http", "SharedState", function (e, t, r, a, n, o, i, l, s) {
    e.configJsApi(["startRecord", "stopRecord", "onVoiceRecordEnd", "uploadVoice"]);
    var c;
    var u = angular.element(document.getElementById("chatContent"));

    function p(e, t) {
        if (/^exam:[0-9]{1,}$/.test(e)) {
            o.get("/server/publics/auth/user/send_exam_report/" + e.substring(5), false, function (e) {
                c = e;
                t != null && t.f(c, t.x)
            }, null, function () {
                c = null
            })
        } else {
            c = null
        }
    }

    function m(e, r, n) {
        if (n == 0) {
            a.cancel(t.voiceDurTimeout);
            return
        }
        l.head(e).then(function (e) {
            n != 5 && a.cancel(t.voiceDurTimeout);
            duration = (e.headers("Content-Length") / 1536).toFixed(0);
            if (duration > 60) {
                duration = 60
            } else if (duration < 1) {
                duration = 1
            }
            r != null && r.f(duration, r.x)
        }, function (o) {
            if (o.status == 404) {
                n--;
                t.voiceDurTimeout = a(function () {
                    m(e, r, n)
                }, 2e3)
            }
        })
    }

    function f() {
        if (t.chatmainPage.elements.length > 0) {
            var e = u.controller("scrollableContent");
            e.scrollTo(document.getElementById("msg" + (t.chatmainPage.elements.length - 1)))
        }
    }

    var d = function () {
        if (t.chatmainPage.elements.length > 0) {
            var e = u.controller("scrollableContent");
            e.scrollTo(document.getElementById("msg" + (t.chatmainPage.elements.length - 1) % 10))
        }
    };
    var g = function (e, r, n, i) {
        if (t.recording) {
            return
        }
        o.get("/server/publics/auth/user/" + t.sessionid + "/message", i, function (e) {
            for (var r in e.content) {
                var n = e.content.length - 1 - r;
                p(e.content[n].message, {
                    f: function (e, r) {
                        t.chatmainPage.elements[r].message = null;
                        t.chatmainPage.elements[r].examReportData = e
                    }, x: r
                });
                if (/^voice:/.test(e.content[n].message)) {
                    e.content[n].voiceData = e.content[n].message.slice(6);
                    e.content[n].message = null
                }
            }
            t.chatmainPage.lastPayload = e;
            t.chatmainPage.elements = e.content.reverse().concat(t.chatmainPage.elements);
            t.chatmainPage.loading = false;
            if (i) {
                a(f, 100)
            } else {
                a(d, 100)
            }
            for (var r = 0; r < t.chatmainPage.lastPayload.numberOfElements; r++) {
                if (t.chatmainPage.elements[r].voiceData) {
                    m(t.chatmainPage.elements[r].voiceData, {
                        f: function (e, r) {
                            t.chatmainPage.elements[r].duration = e
                        }, x: r
                    }, 1)
                }
            }
        }, {params: {page: e, size: r}})
    };
    o.get("/server/publics/auth/user/conversation/id/?counselorId=" + n.counselor_id, true, function (r) {
        t.sessionid = r.id;
        t.checkBalance();
        t.fee = r.counselor.chatUnitPrice;
        t.name = r.counselor.user.nickName;
        e.initTitleDesc(t.name);
        t.counselorid = r.counselor.id;
        t.chatmainPage = i(g, 10)
    });
    t.msgChange = function () {
        t.textMsg = t.messageText != ""
    };
    t.isQuestion;
    t.addMessage = function () {
        if (t.messageText == "") {
            alert("消息不能为空")
        } else {
            p(t.messageText);
            o.post("/server/publics/auth/user/message", false, function (e) {
                t.isQuestion == true && t.checkBalance();
                if (c) {
                    e.message = null;
                    e.examReportData = c
                }
                if (/^voice:/.test(e.message)) {
                    e.voiceData = e.message.slice(6);
                    e.message = null
                }
                t.chatmainPage.elements.push(e);
                a(f, 100);
                t.messageText = "";
                t.textMsg = false;
                if (e.voiceData) {
                    m(e.voiceData, {
                        f: function (e, r) {
                            t.chatmainPage.elements[r].duration = e
                        }, x: t.chatmainPage.elements.length - 1
                    }, 5)
                }
            }, {message: t.messageText, classify: "QUESTION", conversation: {id: t.sessionid}})
        }
    };
    var h = function (e, t, r, a) {
        o.get("/server/publics/auth/user/my_exam_list", a, r, {params: {page: e, size: t}})
    };
    t.reload = function () {
        t.page = i(h, 10)
    };
    t.sendReportFun = function (e) {
        t.messageText = "exam:" + e;
        t.addMessage()
    };
    t.othMsg = false;
    t.voice = false;
    t.recording = false;
    t.voicePlaying = null;
    t.checkBalance = function () {
        o.get("/server/publics/auth/user/" + t.sessionid + "/message/prepare", false, function (a) {
            if (!a) {
                e.showMsgModal({
                    title: "请先充值",
                    content: "<p>您需要充值后才能进行咨询。</p><div>您可以获得如下特权：</div><ul style='padding-left: 20px'><li>发送语音提问<span class='text-danger'>(仅微信下)</span>；</li><li>付费文字消息最多可发300字；</li><li>指定心理测试请咨询师解读。</li></ul><p class='text-center'>【提示】</p><div>问题发起后，咨询师只有做出128字文字消息或45秒以上的语音回复，才会将费用结算给咨询师，咨询师未回复或回复内容不够，则费用会在24小时内退回。</div>",
                    positive: "去充值",
                    negative: "不了",
                    closeBtn: true,
                    onPositive: function () {
                        r.path("/balance/center")
                    },
                    onNegative: function () {
                        t.isQuestion = false;
                        t.othMsg = false;
                        t.voice = false
                    }
                })
            } else {
                t.isQuestion = true;
                t.othMsg = false;
                t.voice = false
            }
        })
    };
    t.switch = function () {
        if (t.recording) {
            return
        }
        if (!e.isWeiXin) {
            e.showMsgModal({
                title: "请在微信中访问该页面",
                content: "语音功能暂时只能在微信中使用，请关注公众号“心情香蕉”。",
                positive: "我知道了",
                onPositive: function () {
                    return
                }
            });
            return
        }
        t.voice = !t.voice;
        t.othMsg = false
    };
    t.record = function () {
        t.othMsg = false;
        t.recording == false && t.startRecord();
        t.recording == true && t.stopRecord()
    };
    t.startRecord = function () {
        t.recordingMask = true;
        wx.ready(function () {
            wx.startRecord({
                success: function () {
                    t.recording = true;
                    t.recordTime = 60;
                    t.backListener = e.$on("$locationChangeStart", function (e) {
                        if (window.confirm("正在录音，确定取消录音？")) {
                            t.backListener();
                            t.stopRecord(true)
                        } else {
                            e.preventDefault()
                        }
                    });
                    t.recordTimeout()
                }, fail: function (e) {
                    alert(e.errMsg)
                }, cancel: function () {
                    alert("您拒绝授权录音")
                }
            })
        })
    };
    t.recordTimeout = function () {
        if (t.recordTime > 0) {
            t.recordingTimeout = a(function () {
                t.recordTime--;
                t.recordTimeout()
            }, 1e3)
        } else {
            t.recordTimeoutCancel()
        }
    };
    t.recordTimeoutCancel = function () {
        t.backListener();
        t.recordTime = 60;
        a.cancel(t.recordingTimeout)
    };
    wx.ready(function () {
        wx.onVoiceRecordEnd({
            complete: function (e) {
                t.recordingMask = false;
                t.recordTimeoutCancel();
                t.localId = e.localId;
                t.recording = false;
                t.uploadVoice()
            }
        })
    });
    t.stopRecord = function (e) {
        t.recordingMask = false;
        wx.ready(function () {
            wx.stopRecord({
                success: function (r) {
                    t.recording = false;
                    t.localId = r.localId;
                    t.recordTimeoutCancel();
                    e != true && t.uploadVoice();
                    t.$apply()
                }, fail: function (e) {
                    alert(e.errMsg)
                }
            })
        })
    };
    t.uploadVoice = function () {
        wx.ready(function () {
            wx.uploadVoice({
                localId: t.localId, isShowProgressTips: 1, success: function (e) {
                    t.messageText = "voice:" + e.serverId;
                    t.addMessage()
                }, fail: function (e) {
                    alert(e.errMsg)
                }
            })
        })
    };
    t.voiceContrl = function (e, r) {
        if (t.recording) {
            return
        }
        if (t.voicePlaying == null) {
            if (r == "failed") {
                alert("语音播放失败，请重新打开页面");
                return
            }
            t.playVoice(e, r)
        } else if (t.voicePlaying == e) {
            t.voicePlaying = null;
            t.stopVoice(e)
        } else {
            t.stopVoice(t.voicePlaying);
            t.voicePlaying = e;
            t.playVoice(e, r)
        }
    };
    t.playVoice = function (e, r) {
        t.voicePlaying = e;
        var a = document.getElementById("audio" + e);
        a.src = r;
        a.play();
        t.hasVoiceEnd(e)
    };
    t.hasVoiceEnd = function (e) {
        var r = document.getElementById("audio" + e);
        if (r.ended) {
            t.voicePlaying = null;
            t.stopVoice(e)
        } else {
            t.voicePlayTimeout = a(function () {
                t.hasVoiceEnd(e)
            }, 1e3)
        }
    };
    t.stopVoice = function (e) {
        a.cancel(t.voicePlayTimeout);
        var r = document.getElementById("audio" + e);
        r.pause();
        r.src = ""
    }
}];
var attenListCtlr = ["$scope", "xxHttp", "xxPage", function (e, t, r) {
    var a = function (e, r, a, n) {
        t.get("/server/publics/auth/user/concern", n, a, {params: {page: e, size: r}})
    };
    e.attenListPage = r(a, 10);
    e.reload = function () {
        r(a, 10)
    }
}];
var applyCounselorCtlr = ["$scope", "$location", "xxHttp", function (e, t, r) {
    r.get("/server/publics/auth/user/counselor_apply", true, function (t) {
        e.cnslrApply = t;
        e.loadSkillsDefault(e.cnslrApply)
    });
    e.loadSkillsDefault = function (t) {
        r.get("/server/publics/counselor_skill", null, function (r) {
            e.skills = r;
            for (var a in r) {
                e.input_skills[r[a].id] = false
            }
            if (t) {
                for (var n in t.skills) {
                    e.input_skills[t.skills[n].id] = true
                }
            }
        })
    };
    e.selectSkill = function (t) {
        var r = 0;
        for (var a in e.input_skills) {
            if (e.input_skills[a]) {
                r++
            }
        }
        if (r >= 2 && !e.input_skills[t.id]) {
            alert("您最多选择2个擅长的领域")
        } else {
            e.input_skills[t.id] = !e.input_skills[t.id]
        }
    };
    e.submit = function () {
        e.cnslrApply.skills = [{id: 0, name: "a"}];
        if (e.cnslrApply.id == null) {
            var a = 0;
            var n = [];
            for (var o in e.input_skills) {
                if (e.input_skills[o]) {
                    n[a] = o;
                    a++
                }
            }
            for (var o = 0; o < a; o++) {
                e.cnslrApply.skills[o] = e.skills[n[o] - 1]
            }
            r.post("/server/publics/auth/user/counselor_apply", null, function (e) {
                alert("您的申请资料已提交成功，工作人员在3个工作日内会联系您核实资料，请保持手机畅通");
                t.path("/").replace()
            }, e.cnslrApply)
        } else {
            var a = 0;
            var n = [];
            for (var o in e.input_skills) {
                if (e.input_skills[o]) {
                    n[a] = o;
                    a++
                }
            }
            for (var o = 0; o < a; o++) {
                e.cnslrApply.skills[o] = e.skills[n[o] - 1]
            }
            r.post("/server/publics/auth/user/counselor_apply", null, function (e) {
                alert("您的申请资料已修改成功");
                t.path("/").replace()
            }, e.cnslrApply)
        }
    }
}];
var noteCtlr = ["$scope", "$routeParams", "xxHttp", function (e, t, r) {
    r.get("/server/publics/counselor/note/" + t.id, true, function (t) {
        e.note = t;
        r.get("/server/publics/counselor/" + t.counselor.id, true, function (t) {
            e.counselor = t
        })
    })
}];
var examCtlr = ["$rootScope", "$scope", "$location", "$routeParams", "$timeout", "xxHttp", "SharedState", function (e, t, r, a, n, o, i) {
    t.answer = [];
    t.farest = 0;
    t.current = 0;
    t.reading = false;
    t.waiting = true;
    t.birthday = e.isUserLogin() && e.user ? new Date(e.user.birthday) : null;
    t.ageLimit = {
        ccbt: {min: 3, max: 18},
        cdi: {min: 7, max: 19},
        cepq: {min: 7, max: 16},
        cpts: {min: 3, max: 8},
        mhsca: {min: 7, max: 13},
        spm: {min: 6, max: 71}
    };
    var l;
    var s = function () {
        o.get("/server/publics/exam_type/" + a.exam_type_id, true, function (a) {
            e.initTitleDesc(a.examType.fullName);
            t.config = a;
            t.step = 1;
            if (r.search().direct) {
                t.examOrBack()
            }
        }, null, function (e, t) {
            alert(t);
            r.path("/exam/list").replace()
        })
    };
    var c = function () {
        o.get("/server/publics/prec/exam_type/" + a.exam_type_id, true, function (r) {
            e.initTitleDesc(r.examType.fullName);
            t.config = r;
            t.step = 1
        }, {params: {member_id: t.groupMember.id, member_serial: t.groupMember.memberSerial}}, function (t, r) {
            alert(r);
            window.location.href = e.rootUrl + "/prec/org/" + a.group_id
        })
    };
    t.saveAnonyExam = function (a, n) {
        n.landing_url = sessionStorage.getItem("landingUrl");
        o.post("/server/publics/exam", function (e) {
            t.submiting = e
        }, function (t) {
            if (sessionStorage.getItem("3rd_exam_report_url")) {
                e.href(sessionStorage.getItem("3rd_exam_report_url"))
            } else {
                localStorage.setItem("anony_exam_ip", t[0].ip);
                r.path("/exam/report/" + t[0].id).replace()
            }
        }, a, {params: n}, function (e, t) {
            alert(t);
            if (e != "NORM_NOT_FOUND") {
                r.path("/exam/list").replace()
            }
        })
    };
    t.savePublicExam = function (a, n) {
        n.landing_url = sessionStorage.getItem("landingUrl");
        o.post("/server/publics/auth/user/exam", function (e) {
            t.submiting = e
        }, function (t) {
            alert("测试报告已为您永久保存。\n您可随时在【个人中心】中查看");
            if (sessionStorage.getItem("3rd_exam_report_url")) {
                e.href(sessionStorage.getItem("3rd_exam_report_url"))
            } else {
                r.path("/exam/report/" + t[0].id).replace()
            }
        }, a, {params: n}, function (e, t) {
            alert(t);
            if (e != "NORM_NOT_FOUND") {
                r.path("/exam/list").replace()
            }
        })
    };
    t.savePrecExam = function (n, i) {
        o.post("/server/publics/prec/exam", function (e) {
            t.submiting = e
        }, function (e) {
            alert("测试报告已为您永久保存。\n您可随时在档案空间中查看");
            r.url("/exam/report/" + e[0].id + "?share_code=" + e[0].shareCode).replace()
        }, n, {params: i}, function (t, r) {
            alert(r);
            if (t != "NORM_NOT_FOUND") {
                window.location.href = e.rootUrl + "/prec/org/" + a.group_id
            }
        })
    };
    t.changeAgree = function () {
        t.refuseAgree = !document.getElementById("agree").checked
    };
    t.examOrBack = function () {
        if (t.refuseAgree) {
            r.path("/")
        } else {
            l = {examTypeId: t.config.examType.id};
            t.step = 2;
            p()
        }
    };
    t.agreeOrDisagree = function (e) {
        document.getElementById("agree").checked = e;
        t.refuseAgree = !e
    };
    var u = function () {
        if (t.config.examType.needGender) {
            if (t.gender == null) {
                alert("请选择您的性别，男左女右^_^");
                return false
            } else {
                l.gender = t.gender
            }
        }
        if (t.config.examType.needBirthday) {
            var e = t.ageLimit[t.config.examType.typeName.toLowerCase()];
            if (t.birthday == null || t.birthday == "") {
                alert("请选择您的生日，公历哦~");
                return false
            } else if (e) {
                var r = (new Date - t.birthday) / 31536e6;
                if (e.min <= r && r < e.max) {
                    l.birthday = t.birthday.getFullYear() + "-" + (t.birthday.getMonth() + 1) + "-" + t.birthday.getDate()
                } else {
                    alert("该测试适用的年龄段为" + e.min + "-" + (e.max - 1) + "岁，请填写正确的年龄或试试其他测试");
                    return false
                }
            } else {
                l.birthday = t.birthday.getFullYear() + "-" + (t.birthday.getMonth() + 1) + "-" + t.birthday.getDate()
            }
        }
        return true
    };
    var p = function () {
        t.startTime = (new Date).getTime();
        t.backListener = e.$on("$locationChangeStart", function (e) {
            if (window.confirm("测试未完成，确定放弃？")) {
                t.backListener()
            } else {
                e.preventDefault()
            }
        });
        n(function () {
            t.waiting = false
        }, 600)
    };
    t.prev = function () {
        t.current--
    };
    t.next = function () {
        t.current++
    };
    t.select = function (e, r) {
        if (t.waiting) {
            return
        }
        t.answer[e] = r;
        if (t.current != t.config.examType.content.length - 1) {
            t.waiting = true;
            n(function () {
                t.current++;
                if (t.farest < t.current) {
                    t.farest++
                }
                t.reading = true;
                n(function () {
                    t.waiting = false;
                    t.reading = false
                }, 600)
            }, 400)
        } else if (t.config.examType.needGender || t.config.examType.needBirthday) {
            t.step = 3
        }
    };
    t.submit = function () {
        if (!u()) {
            return
        }
        var r = t.answer;
        l.totalSeconds = parseInt(((new Date).getTime() - t.startTime) / 1e3);
        l.ads = sessionStorage.getItem("ads");
        t.backListener();
        if (/^[0-9]{1,}$/.test(a.member_id) && /^[0-9]{1,}$/.test(a.group_id)) {
            t.sessionStorageName = "group_" + a.group_id;
            t.groupMember = JSON.parse(sessionStorage.getItem(t.sessionStorageName));
            if (t.groupMember && t.groupMember.id == a.member_id) {
                l.member_id = t.groupMember.id;
                l.member_serial = t.groupMember.memberSerial;
                t.savePrecExam(r, l)
            } else {
                t.savePublicExam(r, l)
            }
        } else if (e.isUserLogin()) {
            t.savePublicExam(r, l)
        } else {
            t.saveAnonyExam(r, l)
        }
    };
    var m = function () {
        if (!sessionStorage.getItem("book_exam_type") && e.showMenu()) {
            t.showJump = true
        }
        if (/^[0-9]{1,}$/.test(a.member_id) && /^[0-9]{1,}$/.test(a.group_id)) {
            t.sessionStorageName = "group_" + a.group_id;
            t.groupMember = JSON.parse(sessionStorage.getItem(t.sessionStorageName));
            if (t.groupMember) {
                t.showJump = false;
                c()
            } else {
                s()
            }
        } else {
            s()
        }
    }()
}];
var finishExamListCtlr = ["$scope", "$rootScope", "xxHttp", "xxPage", "$timeout", "$location", "SharedState", function (e, t, r, a, n, o, i) {
    e.setTime = function (t) {
        e.input_time = e.input_time == t ? null : t
    };
    e.cancelSetTime = function () {
        e.input_time = e.range
    };
    e.cancelSetTypeName = function () {
        if (e.typeName != null) {
            var t = e.typeName.split(",");
            for (var r in e.exam_type_list) {
                for (var a in t) {
                    if (e.exam_type_list[r].typeName != t[a]) {
                        e.exam_type_list[r].selected = false
                    } else {
                        e.exam_type_list[r].selected = true;
                        break
                    }
                }
            }
        } else {
            for (var r in e.exam_type_list) {
                e.exam_type_list[r].selected = false
            }
        }
    };
    var l = function (t, a, n, o) {
        e.range = e.input_time;
        if (e.exam_type_list.length != 0) {
            e.input_type_name = [];
            for (var i in e.exam_type_list) {
                if (e.exam_type_list[i].selected == true) {
                    e.input_type_name.push(e.exam_type_list[i].typeName)
                }
            }
            if (e.input_type_name.length != 0) {
                e.typeName = e.input_type_name.toString()
            } else {
                e.typeName = null
            }
        } else {
            e.typeName = null
        }
        r.get("/server/publics/auth/user/my_exam_list", o, n, {
            params: {
                typeName: e.typeName,
                range: e.range,
                page: t,
                size: a
            }
        })
    };
    e.reload = function () {
        e.page = a(l, 10)
    };
    var s = function () {
        o.search().range && e.setTime(o.search().range.toUpperCase());
        r.get("/server/publics/auth/user/owned_exam_type", true, function (t) {
            e.exam_type_list = t;
            if (o.search().typeName) {
                var r = o.search().typeName.split(",");
                for (var a in r) {
                    for (var n in e.exam_type_list) {
                        if (e.exam_type_list[n].typeName == r[a].toUpperCase()) {
                            e.exam_type_list[n].selected = true
                        }
                    }
                }
            }
            e.reload()
        })
    };
    s();
    e.showTip = function () {
        var e = "<p>因为在" + (t.isWeiXin ? "微信" : "") + (t.isWeiBo ? "微博" : "");
        e += "中已授权登录，这是单独的测试账号，如需查看其它已做测试报告，请点击右上角，选择在";
        e += (t.isIOS ? "Safari" : "") + (!t.isIOS ? "系统浏览器" : "") + "中打开，并以手机号登录。</p>";
        t.showMsgModal({title: "找不到测试报告？", content: e, closeBtn: true})
    }
}];
var examReportCtlr = ["$rootScope", "$scope", "$location", "$timeout", "$routeParams", "$sce", "xxHttp", "SharedState", function (e, t, r, a, n, o, i, l) {
    t.goback = function () {
        history.back()
    };
    t.nStarMarked = 0;
    t.sd1 = {min: 15.866, max: 84.134};
    t.sd2 = {min: 2.275, max: 97.725};
    t.showArticle = function (r, a) {
        t.articleUrl = o.trustAsResourceUrl(r);
        t.articleSandbox = a == null ? "" : a;
        l.turnOn("articleModal");
        var n = e.$on("$locationChangeStart", function (e) {
            e.preventDefault();
            n();
            l.turnOff("articleModal")
        })
    };
    var s = r.search().share_code;
    if (s) {
        i.get("/server/publics/exam/" + n.exam_id + "/share/" + s, true, function (e) {
            t.share = e[0].groupMember == null;
            p(e)
        })
    } else {
        var c = {};
        if (!e.isUserLogin()) {
            c.report = "/server/publics/exam/" + n.exam_id;
            c.order = "/server/publics/exam/order"
        } else {
            c.report = "/server/publics/auth/user/" + n.exam_id + "/exam_report";
            c.order = "/server/publics/auth/user/exam/order"
        }
        i.get(c.report, true, function (r) {
            p(r);
            var a = sessionStorage.getItem("user_seller_id");
            if (t.exam.groupMember == null) {
                i.get(c.order, true, function (r) {
                    t.examOrderState = r;
                    if (t.newExam != null && t.newExam.length > 0) {
                        t.moreInfoTab = "exams"
                    } else if (t.cnslr != null && t.cnslr.length > 0 && e.showCnslr()) {
                        t.moreInfoTab = "cnslr"
                    }
                }, {params: {examId: n.exam_id, seller_id: a}})
            }
        }, {params: {ip: localStorage.getItem("anony_exam_ip")}})
    }

    function u() {
        var a = null;
        if (t.isOwner && t.exam.shareCode) {
            a = r.absUrl().split("?")[0];
            if (n.exam_id == 0) {
                a += t.exam.id
            }
            a = a + "?share_code=" + t.exam.shareCode
        } else {
            a = e.rootUrl + "/exam/" + t.exam.examType.id + "/null/null"
        }
        if (e.seller) {
            a = a + (t.exam.shareCode ? "&" : "?") + "slr=" + e.seller.id
        }
        if (t.exam.user) {
            if (t.exam.user.icon) {
                var o = e.getPhoto(t.exam.user.icon)
            } else {
                var o = e.getPhoto(t.exam.examType.photo, "?x-oss-process=style/11s")
            }
        } else {
            var o = e.getPhoto(t.exam.examType.photo, "?x-oss-process=style/11s")
        }
        e.wxShare(e.idx_title, a, o, e.idx_desc)
    }

    function p(r) {
        t.exam = r[0];
        t.cnslr = r[1];
        t.newExam = r[2];
        t.detail = t.exam.showDetailReport || t.exam.groupMember != null && t.exam.groupMember.memberBatch.showReport == 2;
        t.isOwner = t.exam.groupMember != null || e.isUserLogin() && e.user.id == t.exam.user.id;
        e.initTitleDesc(t.exam.examType.fullName + "报告", t.exam.examType.introduction);
        a(u, 500);
        if (t.exam.examType.typeName == "16PF") {
            var n = function (e, t) {
                return t.v - e.v
            };
            t.arr16pf = [{k: "A", v: t.exam.stdA}, {k: "B", v: t.exam.stdB}, {k: "C", v: t.exam.stdC}, {
                k: "E",
                v: t.exam.stdE
            }, {k: "F", v: t.exam.stdF}, {k: "G", v: t.exam.stdG}, {k: "H", v: t.exam.stdH}, {
                k: "I",
                v: t.exam.stdI
            }, {k: "L", v: t.exam.stdL}, {k: "M", v: t.exam.stdM}, {k: "N", v: t.exam.stdN}, {
                k: "O",
                v: t.exam.stdO
            }, {k: "Q1", v: t.exam.stdQ1}, {k: "Q2", v: t.exam.stdQ2}, {k: "Q3", v: t.exam.stdQ3}, {
                k: "Q4",
                v: t.exam.stdQ4
            }, {k: "Y3", v: t.exam.stdY3}, {k: "Y4", v: t.exam.stdY4}];
            t.arr16pf.sort(n)
        }
    }

    t.deepReport = function () {
        var a = sessionStorage.getItem("user_seller_id");
        if (e.isUserLogin()) {
            i.get("/server/publics/auth/user/exam/order", true, function (e) {
                t.examOrderState = e;
                var a = {
                    examId: t.exam.id,
                    examTypeCode: t.exam.examType.typeName,
                    examTypeName: t.exam.examType.fullName,
                    examOrderPrice: e.orderPrice,
                    examTypeFee: e.fee,
                    examPhoto: t.exam.examType.photo,
                    balance: e.balance
                };
                localStorage.setItem("examOrderData", JSON.stringify(a));
                r.path("/pay/exam")
            }, {params: {examId: t.exam.id, seller_id: a}})
        } else {
            i.get("/server/publics/exam/order", true, function (e) {
                t.examOrderState = e;
                var a = {
                    examId: t.exam.id,
                    examTypeCode: t.exam.examType.typeName,
                    examTypeName: t.exam.examType.fullName,
                    examOrderPrice: e.orderPrice,
                    examTypeFee: e.fee,
                    examPhoto: t.exam.examType.photo,
                    balance: e.balance
                };
                localStorage.setItem("examOrderData", JSON.stringify(a));
                r.path("/pay/exam")
            }, {params: {examId: t.exam.id, seller_id: a}})
        }
    };
    t.clickCnslr = function (t) {
        e.showMsgModal({
            title: "向咨询师发送报告",
            content: '进入咨询界面后，选择付费问答，点击右下角的 <i class="fa fa-plus-circle"></i> 即可选择发送报告。',
            negative: "不了",
            positive: "现在就去",
            closeBtn: true,
            onPositive: function () {
                r.path("/chat/main/" + t)
            },
            onNegative: function () {
            }
        })
    }
}];
var examListCtlr = ["$rootScope", "$scope", "xxHttp", "xxPage", "$location", function (e, t, r, a, n) {
    var o = function (e, a, n, o) {
        r.get("/server/publics/exam_type", o, n, {params: {classify: t.classify, page: e, size: a}})
    };
    t.reload = function () {
        t.page = a(o, 10);
        if (e.isUserLogin()) {
            r.get("/server/publics/auth/user/finish_exam_type_ids", true, function (e) {
                t.finishExamTypeIds = e[0];
                t.finishExamIds = e[1]
            })
        }
    };
    t.switchClassify = function (e) {
        t.classify = e;
        n.search("classify", e);
        t.reload()
    };
    var i = function () {
        t.classify = n.search().classify;
        t.classify = t.classify == null ? "HEALTH" : t.classify;
        t.reload()
    }();
    t.examOrReport = function (r) {
        if (e.isUserLogin() && t.finishExamTypeIds.indexOf(r) >= 0) {
            e.showMsgModal({
                title: "提示",
                content: "立即查看结果？",
                negative: "再次测试",
                positive: "查看报告",
                closeBtn: true,
                onPositive: function () {
                    n.path("/exam/report/" + t.finishExamIds[t.finishExamTypeIds.indexOf(r)])
                },
                onNegative: function () {
                    n.path("/exam/" + r + "/null/null")
                }
            })
        } else {
            n.path("/exam/" + r + "/null/null")
        }
    }
}];
var examOrderCtlr = ["$rootScope", "$scope", "$location", "$document", "$window", "xxHttp", function (e, t, r, a, n, o) {
    var i = function () {
        window._agl && window._agl.push(["track", ["success", {t: 3}]]);
        localStorage.removeItem("examOrderData");
        r.path("/exam/report/" + t.examOrderData.examId).replace()
    };
    var l = function () {
        o.post("/server/publics/auth/user/" + t.examOrderData.examId + "/balance_order_exam/", true, function (e) {
            i()
        }, null, {params: t.params}, function (e, a) {
            alert(a);
            r.path("/exam/report/" + t.examOrderData.examId)
        })
    };
    t.alipay = function () {
        o.get("/server/publics/auth/user/" + t.examOrderData.examId + "/alipay_order_exam/", true, function (e) {
            n.location.href = e
        }, {params: t.params})
    };
    var s = function (e) {
        if (e.result != null) {
            o.post("/server/publics/auth/user/charge/alipay/wap", true, function (e) {
                i()
            }, {
                result: e.result,
                sign: e.sign,
                out_trade_no: e.out_trade_no,
                trade_no: e.trade_no,
                request_token: e.request_token
            })
        }
    };
    var c = function () {
        r.search("showwxpaytitle", 1);
        n.location.href = r.absUrl()
    };
    var u = function () {
        var n;
        t.startWeiXinPay = function () {
            e.loading = e.loadingBlock = true;
            WeixinJSBridge.invoke("getBrandWCPayRequest", n, function (a) {
                if (a.err_msg == "get_brand_wcpay_request:ok") {
                    localStorage.setItem("weixinOrderExamSucceed", true)
                } else {
                    alert("订购测试报告失败!请重新支付[" + a.err_msg + "]")
                }
                r.search("showwxpaytitle", null);
                t.$apply();
                e.loading = e.loadingBlock = false
            });
            t.$apply()
        };
        if (r.search().showwxpaytitle == 1) {
            o.post("/server/publics/auth/user/" + t.examOrderData.examId + "/weixin_order_exam/", true, function (e) {
                n = e[0];
                localStorage.setItem("flowId", e[1]);
                if (typeof WeixinJSBridge == "undefined") {
                    a.bind("WeixinJSBridgeReady", t.startWeiXinPay)
                } else {
                    t.startWeiXinPay()
                }
            }, JSON.parse(localStorage.getItem("user_token")).wxOpenUser.openId, {params: t.params})
        }
    };
    var p = function () {
        o.get("/server/publics/exam/" + t.examOrderData.examId + "/wx_h5_pay", true, function (r) {
            if (e.isPC) {
                t.qr = r
            } else {
                localStorage.setItem("wx_h5_pay", true);
                t.h5BackNoInit = true;
                n.location.href = r
            }
        }, {params: t.params})
    };
    t.verifyWxH5Pay = function () {
        o.get("/server/publics/exam/" + t.examOrderData.examId + "/order", true, function (r) {
            if (r) {
                localStorage.removeItem("wx_h5_pay");
                sessionStorage.setItem("goWX", true);
                i()
            } else {
                e.showMsgModal({
                    title: "付款确认中",
                    content: "你是否已完成支付？\n因网络延迟，请稍候再点【已完成】",
                    positive: "已完成",
                    negative: "重新支付",
                    onPositive: function () {
                        t.verifyWxH5Pay()
                    },
                    onNegative: function () {
                        t.h5BackNoInit = false
                    }
                })
            }
        })
    };
    t.pay = function () {
        if (!e.isUserLogin()) {
            p()
        } else if (t.examOrderData.balance >= t.examOrderData.examTypeFee) {
            l()
        } else if (e.isWeiXin) {
            e.requestWeiXinPay = true;
            c()
        } else {
            t.alipay()
        }
    };
    var m = function () {
        var a = sessionStorage.getItem("user_seller_id");
        t.params = {slr: a != null && !isNaN(a) ? a : null, is_pc: e.isPC};
        var n = localStorage.getItem("examOrderData");
        var l = localStorage.getItem("flowId");
        var c = localStorage.getItem("weixinOrderExamSucceed");
        if (n) {
            t.examOrderData = JSON.parse(n);
            if (!e.isUserLogin()) {
                if (localStorage.getItem("wx_h5_pay") != null) {
                    t.verifyWxH5Pay()
                }
            } else if (e.isWeiXin) {
                if (l != null && c != null) {
                    o.get("/server/publics/auth/user/order_exam_succeed/transid?flowId=" + l, true, function (e) {
                        localStorage.removeItem("flowId");
                        localStorage.removeItem("weixinOrderExamSucceed");
                        i()
                    })
                } else if (!e.requestWeiXinPay) {
                    u()
                }
            } else {
                var p = r.search();
                if (p.result != null) {
                    s(p)
                }
            }
        } else {
            r.path("/")
        }
    }()
}];
var settingsCtlr = ["$rootScope", "$scope", "$location", "xxHttp", function (e, t, r, a) {
    t.confirmLogout = function () {
        if (e.isQQ || e.isWeiXin || e.isWeiBo) {
            return
        }
        e.showMsgModal({
            title: "退出登录",
            content: "清除当前登录身份?",
            negative: "保持登录",
            positive: "确认退出",
            onPositive: function () {
                a.get("/server/publics/user/logout", true, function (e) {
                }, null, function (e, t) {
                    cookie.remove("user_token")
                }, function (e, t, r) {
                    cookie.remove("user_token")
                });
                r.path("/").replace()
            }
        })
    }
}];
var myPhpCtlr = ["$rootScope", "$scope", "$location", "$window", "xxHttp", function (e, t, r, a, n) {
    if (e.isUserLogin()) {
        n.get("/server/publics/auth/user/php", true, function (e) {
            t.php = e[0];
            t.lockList = e[1]
        })
    }
    t.openForNew = function () {
        if (sessionStorage.getItem("goWX") != null) {
            e.showMsgModal({
                title: "前往公众号查看",
                content: "档案已保存在支付的微信账号下，请关注微信公众号后查看。",
                positive: "去关注",
                closeBtn: true,
                onPositive: function () {
                    if (e.wxJump != null) {
                        a.location.href = e.wxJump
                    } else {
                        alert("请关注微信公众号【心情香蕉】")
                    }
                }
            })
        } else {
            e.showMsgModal({
                title: "首次开启档案",
                content: "请选择您更想了解的方向，完成对应专业测试以解锁",
                positive: "人格特质",
                negative: "心理健康",
                closeBtn: true,
                onPositive: function () {
                    r.path("/exam/16PF/null/null")
                },
                onNegative: function () {
                    r.path("/exam/SCL90/null/null")
                }
            })
        }
    }
}];
var salesCtlr = ["$rootScope", "$scope", "xxHttp", "SharedState", function (e, t, r, a) {
    e.loadSeller(true);
    t.submit = function () {
        if (confirm("确认成为中国人心智调研员？")) {
            var t = sessionStorage.getItem("user_seller_id");
            t = t != null && !isNaN(t) ? t : null;
            r.post("/server/publics/auth/user/sales/seller", true, function (t) {
                e.loadSeller(true)
            }, t)
        }
    };
    t.changeRatio = function () {
        t.change_ratio = e.seller.priceRatio;
        a.turnOn("changeRatioModal")
    };
    t.submitChangeRatio = function (t) {
        r.put("/server/publics/auth/user/sales/seller", true, function () {
            a.turnOff("changeRatioModal");
            e.loadSeller(true)
        }, {priceRatio: t}, {params: {action: "change_ratio"}})
    }
}];
var salesLinksCtlr = ["$rootScope", "$scope", "xxHttp", "xxPage", function (e, t, r, a) {
    e.loadSeller();
    var n = function (e, t, a, n) {
        r.get("/server/publics/exam_type", n, a, {params: {page: e, size: t}})
    };
    t.exams = a(n, 10);
    t.noCnslr = sessionStorage.getItem("no_cnslr") != null;
    t.switchNoCnslr = function () {
        t.noCnslr = !t.noCnslr;
        if (t.noCnslr) {
            sessionStorage.setItem("no_cnslr", true)
        } else {
            sessionStorage.removeItem("no_cnslr")
        }
    }
}];
var salesBrokerageCtlr = ["$rootScope", "$scope", "xxHttp", "xxPage", "SharedState", function (e, t, r, a, n) {
    e.loadSeller();
    var o = function (e, t, a, n) {
        r.get("/server/publics/auth/user/sales/brokerage", n, a, {params: {page: e, size: t}})
    };
    t.flows = a(o, 10);
    t.submit = function () {
        if (confirm("确认提现至支付宝账户" + t.info.alipayAccount + "？")) {
            r.post("/server/publics/auth/user/sales/brokerage", true, function (r) {
                e.loadSeller(true);
                t.flows = a(o, 10);
                alert("提现申请已提交！");
                n.turnOff("brokerage")
            }, t.info)
        }
    };
    t.request = function () {
        if (e.user.mobile) {
            t.info = {alipayName: e.seller.alipayName, alipayAccount: e.seller.alipayAccount};
            n.turnOn("brokerage")
        } else {
            alert("请验证手机号，方便工作人员联系您");
            n.turnOn("bindMobileModal")
        }
    }
}];
var salesOrderListCtlr = ["$rootScope", "$scope", "xxHttp", "xxPage", function (e, t, r, a) {
    e.loadSeller();
    var n = function (e, a, n, o) {
        r.get("/server/publics/auth/user/sales/order_list", o, n, {params: {page: e, size: a, referral: t.referral}})
    };
    t.reload = function (e) {
        t.referral = e;
        t.orders = a(n, 10)
    };
    t.reload(false)
}];
var salesReferralCtlr = ["$rootScope", "$scope", "xxHttp", "xxPage", function (e, t, r, a) {
    e.loadSeller();
    var n = function (e, t, a, n) {
        r.get("/server/publics/auth/user/sales/seller/referral", n, a, {params: {page: e, size: t}})
    };
    t.referrals = a(n, 10)
}];
var packCtrl = ["$rootScope", "$scope", "$location", "xxHttp", function (e, t, r, a) {
    var n = {
        health: ["sas", "sds", "scl90"],
        career: ["eqt", "wpmf", "mbti", "nine_house"],
        emotion: ["hst", "temperament", "nine_house"]
    };
    sessionStorage.removeItem("3rd_exam_report_url");
    var o = r.path();
    var i = n[o.substring(o.lastIndexOf("/") + 1)];

    function l(e) {
        a.get("/server/publics/auth/user/exam/last?type=" + i[e], true, function (r) {
            t[i[e]] = r
        })
    }

    if (e.isUserLogin()) {
        for (var s in i) {
            l(s)
        }
    }
    t.goNewExam = function (e) {
        t.examTypeName = e;
        sessionStorage.setItem("3rd_exam_report_url", r.absUrl());
        r.path("/exam/" + t.examTypeName + "/null/null")
    }
}];