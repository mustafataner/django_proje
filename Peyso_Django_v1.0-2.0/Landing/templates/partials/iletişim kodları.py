'''


{% load static %}
{% block contact %}
   <!-- Start contact -->
   <section id="contact">
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <div class="card contact-section-card mb-0">
                    <div class="card-body p-md-5">
                        <div class="text-center title mb-5">
                            <p class="text-muted text-uppercase fw-normal mb-2">İletişim</p>
                            <h3 class="mb-3">Bir sorunuz mu var?</h3>
                            <div class="title-icon position-relative">
                                <div class="position-relative">
                                    <i class="uim uim-arrow-circle-down"></i>
                                </div>
                            </div>
                        </div>

                        <!-- start form -->
                        <form method="post" name="myForm" onsubmit="return validateForm()" href="javascript: void(0);">
                            <p id="error-msg"></p>
                            <div class="row">
                                <div class="col-lg-6">
                                    <div class="mb-3">
                                        <label class="form-label" for="name">Adınız</label>
                                        <input name="name" id="name" type="text" class="form-control" placeholder="Lütfen adınızı giriniz..." />
                                    </div>
                                </div>
                                <div class="col-lg-6">
                                    <div class="mb-3">
                                        <label class="form-label" for="email">Email Adres</label>
                                        <input name="email" id="email" type="email" class="form-control" placeholder="Lütfen Mail adresini giriniz..." />
                                    </div>
                                </div>
                            </div>
                            <!-- end row -->

                            <div class="mb-3">
                                <label class="form-label" for="subject">Konu</label>
                                <input name="subject" id="subject" type="text" class="form-control" placeholder="Lütfen konuyu yazınız..." />
                            </div>

                            <div class="mb-3">
                                <label class="form-label" for="comments">Mesajınız</label>
                                <textarea name="comments" id="comments" rows="3" class="form-control" placeholder="Lütfen sorunuzu detaylı yazınız..."></textarea>
                            </div>

                            <div class="text-end">
                                <input type="submit" id="submit" name="send" class="submitBnt btn btn-primary" value="Gönder!" />

                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <!-- end row -->
    </div>
    <!-- end container -->
</section>
<!-- end contact -->
{% endblock contact %}
'''
